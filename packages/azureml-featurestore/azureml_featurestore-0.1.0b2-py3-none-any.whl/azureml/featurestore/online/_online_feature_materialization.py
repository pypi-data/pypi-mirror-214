# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from azureml.featurestore._feature_set import FeatureSet
from azureml.featurestore._utils._constants import TIME_TO_LIVE
from azureml.featurestore.contracts.store_connection import OnlineStoreType
from azureml.featurestore.online._redis_client_pool import _get_redis_connection_string
from ._utils import _get_lookup_key, _get_lookup_key_udf, _get_lookup_key_pattern


def materialize_online(feature_set, dataframe_to_store, upsert):
    # Do the 3 steps
    from pyspark.sql import SparkSession

    spark = SparkSession.builder.getOrCreate()
    # Repartition the data
    # Figure out the header rows
    key_index_column = feature_set.get_index_columns()
    # Extract only the name from the column object
    key_index_column = [x.name for x in key_index_column]
    # Rest of the header will be feature values to store
    value_columns = [x for x in dataframe_to_store.schema.names if x not in key_index_column]

    from pyspark.sql import Window
    from pyspark.sql.functions import col, current_timestamp, desc, rank, unix_timestamp

    # This process is needed because it is possible that we have rows with duplicate key.
    # We will only keep the key with the latest timestamp
    # Rank each row by the key columns ordered by timestmap. Take the largest timestamp
    time_stamp, _ = feature_set.get_timestamp_column()
    win_spec = Window.partitionBy([col(x) for x in key_index_column]).orderBy(desc(time_stamp))
    dataframe_to_store = (
        dataframe_to_store.withColumn("rank", rank().over(win_spec)).select("*").where("rank = 1").drop("rank")
    )
    if feature_set.temporal_join_lookback:
        cur_time_unix = unix_timestamp(current_timestamp())
        temporal_lookback = feature_set.temporal_join_lookback.to_timedelta()
        temporal_lookback_seconds = temporal_lookback.total_seconds()
        df = dataframe_to_store.withColumn(
            TIME_TO_LIVE, temporal_lookback_seconds - (cur_time_unix - unix_timestamp(dataframe_to_store[time_stamp]))
        )
        dataframe_to_store = df.filter(df[TIME_TO_LIVE] > 0)

    number_of_materialized_rows = dataframe_to_store.count()

    feature_set_time_stamp, _ = feature_set.get_timestamp_column()
    prefix, suffix_columns = _get_lookup_key_pattern(feature_set)

    def saveIntoRedisRecurringJob(rdd, redis_connection_string, value_columns):
        # Save every record into redis without caring about timestamp.
        # Replacement operation
        from redis import Redis

        redis_client = Redis.from_url(redis_connection_string)
        pipe = redis_client.pipeline()
        for record in rdd:
            primaryKey = _get_lookup_key_udf(prefix, suffix_columns, record)
            # Set is upsert. Replace if exist
            for value_column in value_columns:
                pipe.hset(primaryKey, value_column, str(record[value_column]))
            if TIME_TO_LIVE in record:
                pipe.expire(primaryKey, int(record[TIME_TO_LIVE]))
        pipe.execute()

    def saveIntoRedisBackfillJob(rdd, redis_connection_string, value_columns):
        # Fetch each record from redis and compare timestamp before saving
        from dateutil.parser import parse
        from redis import Redis

        redis_client = Redis.from_url(redis_connection_string)
        pipe = redis_client.pipeline()
        time_stamp = feature_set_time_stamp
        for record in rdd:
            primaryKey = _get_lookup_key_udf(prefix, suffix_columns, record)
            # TODO change timestamp to the correct timestamp column value
            redis_record_timestamp = redis_client.hget(primaryKey, time_stamp)
            if redis_record_timestamp is not None:
                redis_record_timestamp = parse(redis_record_timestamp)
            current_record_timestamp = parse(str(record[time_stamp]))
            if redis_record_timestamp is None or current_record_timestamp >= redis_record_timestamp:
                for value_column in value_columns:
                    pipe.hset(primaryKey, value_column, str(record[value_column]))
            if TIME_TO_LIVE in record:
                pipe.expire(primaryKey, int(record[TIME_TO_LIVE]))
        pipe.execute()

    if not feature_set.online_store.target:
        raise Exception(
            f'Featureset "{feature_set.arm_id}" belongs to a featurestore that does not specify an online store connection.'
        )

    if feature_set.online_store.type != OnlineStoreType.REDIS:
        raise Exception(
            f'Featureset "{feature_set.arm_id}" specifies an online store connection of type "{feature_set.online_store.type}". Only "redis" online stores are currently supported.'
        )

    from azure.ai.ml.identity import AzureMLOnBehalfOfCredential

    # Get the redis connection string
    credential = AzureMLOnBehalfOfCredential()
    redis_connection_string = _get_redis_connection_string(feature_set.online_store.target, credential)

    if upsert:
        dataframe_to_store.rdd.foreachPartition(
            lambda x: saveIntoRedisBackfillJob(x, redis_connection_string, value_columns)
        )
    else:
        dataframe_to_store.rdd.foreachPartition(
            lambda x: saveIntoRedisRecurringJob(x, redis_connection_string, value_columns)
        )

    return number_of_materialized_rows
