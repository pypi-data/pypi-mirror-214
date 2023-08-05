# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import importlib
import os
from datetime import datetime
from typing import List, Tuple

from azureml.featurestore._utils._constants import (
    CREATE_TIMESTAMP_COLUMN,
    PARTITION_COLUMN,
    SYS_CREATE_TIMESTAMP_COLUMN,
    SYS_UPDATE_TIMESTAMP_COLUMN,
)
from azureml.featurestore._utils.error_constants import (
    SCHEMA_ERROR_NO_INDEX_COLUMN,
    SCHEMA_ERROR_NO_TIMESTAMP_COLUMN,
    SCHEMA_ERROR_WRONG_DATA_TYPE,
)
from azureml.featurestore._utils.type_map import TypeMap
from azureml.featurestore.contracts.datetimeoffset import DateTimeOffset
from azureml.featurestore.contracts.feature import Feature
from azureml.featurestore.contracts.feature_source import SourceType
from azureml.featurestore.contracts.partition import Partition
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, lit, rand, row_number, to_timestamp
from pyspark.sql.types import TimestampType
from pyspark.sql.window import Window

from azure.ai.ml.entities import DataColumn
from azure.ai.ml.exceptions import ErrorCategory, ErrorTarget, ValidationErrorType, ValidationException


def _load_source_data(
    spark: SparkSession,
    source_type: SourceType,
    source_path: str,
    timestamp_column: str,
    timestamp_column_format: str = None,
    source_lookback: DateTimeOffset = None,
    feature_window_start_time: datetime = None,
    feature_window_end_time: datetime = None,
) -> DataFrame:

    if source_type == SourceType.CSV:
        source_df = spark.read.csv(source_path, inferSchema=True, header=True)
    elif source_type == SourceType.PARQUET:
        source_df = spark.read.parquet(source_path)
    elif source_type == SourceType.MLTABLE:
        source_df = spark.read.mltable(source_path)
    elif source_type == SourceType.DELTATABLE:
        source_df = spark.read.format("delta").load(source_path)
    else:
        raise Exception("Feature source type: {} is not supported".format(source_type))

    if not timestamp_column:
        return source_df

    source_df, timestamp_column = _source_timestamp_check(
        df=source_df, timestamp_column=timestamp_column, timestamp_column_format=timestamp_column_format
    )

    if feature_window_start_time:
        source_window_start_time = feature_window_start_time
        # If source lookback is not provided, assume data does not use aggregation outside the time window
        if source_lookback:
            source_window_start_time = source_window_start_time - source_lookback.to_timedelta()
        source_df = source_df.filter(col(timestamp_column) >= to_timestamp(lit(source_window_start_time)))

    if feature_window_end_time:
        source_df = source_df.filter(col(timestamp_column) < to_timestamp(lit(feature_window_end_time)))

    return source_df


def _transform_dataframe(
    spark: SparkSession, source_df: DataFrame, transformer_code_path: str, transformer_class: str
) -> DataFrame:
    strs = transformer_class.split(".")
    pyfile = "{}".format(strs[0])
    class_name = strs[1]

    # Transformer code path is a zip with namespace
    spark.sparkContext.addPyFile(transformer_code_path)

    file_name = os.path.basename(transformer_code_path)
    namespace = os.path.splitext(file_name)[0]
    module = importlib.import_module(name=f"{namespace}.{pyfile}")
    _class = getattr(module, class_name)
    transformer = _class()

    df = transformer.transform(source_df)

    return df


def _filter_dataframe(
    spark: SparkSession,
    df: DataFrame,
    featureWindowStartDateTime: datetime,
    featureWindowEndDateTime: datetime,
    index_columns: List[str],
    timestamp_column: str,
    features: List[str],
) -> DataFrame:
    # filter the dataframe to the given feature window and remove intermediate rows from source lookback (if any)
    if featureWindowStartDateTime:
        df = df.filter(col(timestamp_column) >= to_timestamp(lit(featureWindowStartDateTime)))

    if featureWindowEndDateTime:
        df = df.filter(col(timestamp_column) < to_timestamp(lit(featureWindowEndDateTime)))

    columns = index_columns
    if CREATE_TIMESTAMP_COLUMN in df.columns:
        columns.append(CREATE_TIMESTAMP_COLUMN)
    if timestamp_column:
        columns.append(timestamp_column)
    columns += features

    df = df.select(*columns)

    return df


def _source_schema_check(df: DataFrame, features: List[Feature], index_columns: List[DataColumn]):
    for feature in features:
        if feature.name not in df.columns:
            raise Exception("Schema check errors, no feature column: {} in output dataframe".format(feature.name))
        data_type = TypeMap.spark_to_column_type(df.schema[feature.name].dataType.typeName())
        expected_data_type = feature.type
        if data_type != expected_data_type:
            raise ValidationException(
                message=SCHEMA_ERROR_WRONG_DATA_TYPE.format(feature.name, data_type, expected_data_type),
                no_personal_data_message=SCHEMA_ERROR_WRONG_DATA_TYPE,
                error_type=ValidationErrorType.MISSING_FIELD,
                error_category=ErrorCategory.USER_ERROR,
                target=ErrorTarget.GENERAL,
            )

    for index_column in index_columns:
        if index_column.name not in df.columns:
            raise Exception(SCHEMA_ERROR_NO_INDEX_COLUMN.format(index_column.name))
        data_type = TypeMap.spark_to_column_type(df.schema[index_column.name].dataType.typeName())
        expected_data_type = index_column.type
        if data_type != expected_data_type:
            raise ValidationException(
                message=SCHEMA_ERROR_WRONG_DATA_TYPE.format(index_column.name, data_type, expected_data_type),
                no_personal_data_message=SCHEMA_ERROR_WRONG_DATA_TYPE,
                error_type=ValidationErrorType.MISSING_FIELD,
                error_category=ErrorCategory.USER_ERROR,
                target=ErrorTarget.GENERAL,
            )

    return df, list(map(lambda i: i.name, index_columns))


def _source_timestamp_check(
    df: DataFrame,
    timestamp_column: str,
    timestamp_column_format: str,
):
    if not timestamp_column:
        return df, timestamp_column

    if timestamp_column in df.columns:
        if df.schema[timestamp_column].dataType != TimestampType():
            if timestamp_column_format:
                df = df.withColumn(timestamp_column, to_timestamp(timestamp_column, timestamp_column_format))
            else:
                df = df.withColumn(timestamp_column, to_timestamp(timestamp_column))
    else:
        raise ValidationException(
            message=SCHEMA_ERROR_NO_TIMESTAMP_COLUMN.format(timestamp_column),
            no_personal_data_message=SCHEMA_ERROR_NO_TIMESTAMP_COLUMN,
            error_type=ValidationErrorType.MISSING_FIELD,
            error_category=ErrorCategory.USER_ERROR,
            target=ErrorTarget.GENERAL,
        )

    return df, timestamp_column


def _deduplicate_dataframe(df: DataFrame, join_keys: List[str], timestamp_column: str) -> Tuple[DataFrame, bool]:
    # check duplicated rows in input data, and help deduplicate
    if len(df.groupBy(join_keys + [timestamp_column]).count().filter(col("count") > 1).take(1)) > 0:
        if CREATE_TIMESTAMP_COLUMN in df.columns:
            w2 = Window.partitionBy(join_keys + [timestamp_column]).orderBy(col(CREATE_TIMESTAMP_COLUMN).desc())
        else:
            w2 = Window.partitionBy(join_keys + [timestamp_column]).orderBy(rand())
        distinct_df = df.withColumn("row", row_number().over(w2)).filter(col("row") == 1).drop("row")

        return distinct_df, True
    else:
        return df, False


def build_update_feature_mapping(source_prefix, feature_names):
    mapping = {
        CREATE_TIMESTAMP_COLUMN: f"{source_prefix}.{CREATE_TIMESTAMP_COLUMN}",
        SYS_UPDATE_TIMESTAMP_COLUMN: f"{source_prefix}.{SYS_UPDATE_TIMESTAMP_COLUMN}",
    }
    for feature_name in feature_names:
        mapping[feature_name] = f"{source_prefix}.{feature_name}"

    return mapping


def build_insert_feature_mapping(source_prefix, join_keys, feature_names, timestamp_column):
    mapping = build_update_feature_mapping(source_prefix, feature_names)
    mapping[SYS_CREATE_TIMESTAMP_COLUMN] = f"{source_prefix}.{SYS_CREATE_TIMESTAMP_COLUMN}"
    mapping[timestamp_column] = f"{source_prefix}.{timestamp_column}"
    mapping[PARTITION_COLUMN] = f"{source_prefix}.{PARTITION_COLUMN}"

    for join_key in join_keys:
        mapping[join_key] = f"{source_prefix}.{join_key}"

    return mapping


def build_merge_condition(join_keys, source_prefix, target_prefix, timestamp_column, partition_list):
    partition_str = ",".join(f"'{partition}'" for partition in partition_list)
    arr = [
        f"{target_prefix}.{PARTITION_COLUMN} IN ({partition_str})",
        f"{source_prefix}.{timestamp_column} = {target_prefix}.{timestamp_column}",
    ]
    for join_key in join_keys:
        arr.append(f"{source_prefix}.{join_key} = {target_prefix}.{join_key}")
    return " AND ".join(arr)


def build_updated_timestamp_merge_condition(source_prefix, target_prefix):
    return f"{source_prefix}.{CREATE_TIMESTAMP_COLUMN} > {target_prefix}.{CREATE_TIMESTAMP_COLUMN}"


def build_partition_list(partition: Partition):
    # place holder for changing partition strategy
    return partition.partition_column
