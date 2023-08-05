# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import json
import re
from collections import OrderedDict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Union

import requests
from azureml.featurestore import FeatureSetSpec
from azureml.featurestore._utils._constants import PACKAGE_NAME, PARTITION_COLUMN
from azureml.featurestore._utils.error_constants import (
    FEATURE_NAME_NOT_FOUND_FEATURE_SET,
    FEATURE_NAME_NOT_STRING_FEATURE_SET,
    FEATURE_SET_NOT_REGISTERED,
    MISSING_TIMESTAMP_COLUMN,
)
from azureml.featurestore._utils.utils import _build_logger
from azureml.featurestore.contracts.column import Column, ColumnType
from marshmallow import EXCLUDE

from azure.ai.ml import MLClient
from azure.ai.ml._exception_helper import log_and_raise_error
from azure.ai.ml._restclient.v2023_04_01_preview.models import FeaturesetVersion
from azure.ai.ml._schema._feature_set import MaterializationSettingsSchema
from azure.ai.ml._telemetry.activity import ActivityType, log_activity, monitor_with_activity
from azure.ai.ml._utils._arm_id_utils import get_arm_id_object_from_id
from azure.ai.ml.constants._common import BASE_PATH_CONTEXT_KEY, SHORT_URI_FORMAT
from azure.ai.ml.entities import FeatureSetSpecification, FeatureStoreEntity, MaterializationSettings
from azure.ai.ml.entities._assets import Artifact
from azure.ai.ml.entities._assets._artifacts.artifact import ArtifactStorageInfo
from azure.ai.ml.exceptions import ErrorCategory, ErrorTarget, MlException, ValidationErrorType, ValidationException
from azure.ai.ml.operations import DatastoreOperations

package_logger = None


def _get_logger():
    global package_logger
    if package_logger is None:
        package_logger = _build_logger(__name__)
    return package_logger


class FeatureSet(Artifact):
    """Represents a data plane feature set asset.

    You should not instantiate this class directly. Instead, you should create a FeatureStoreClient instance and get it
    for you by calling FeatureStoreClient.feature_sets.get().
    """

    def __init__(
        self,
        *,
        name: str,
        version: str,
        entities: Union[List[str], List[FeatureStoreEntity]],
        materialization_settings: Optional[MaterializationSettings] = None,
        specification: Optional[FeatureSetSpecification] = None,
        description: Optional[str] = None,
        stage: Optional[str] = None,
        datastore_operations: Optional[DatastoreOperations] = None,
        tags: Optional[Dict[str, str]] = None,
        **kwargs,
    ):
        """Initialize a feature set asset.

        :param name: The feature set asset name
        :type name: str
        :param version: The feature set asset version
        :type version: str
        :param description: The feature set asset description
        :type description: str
        :param specification: Path to feature set specification folder. Can be local or cloud
        :type specification: FeatureSetSpecification
        :param entities: List of entities in the feature set
        :type entities: List[FeatureStoreEntity]
        :param materialization_settings: Materialization settings control the strategy and
                                        frequency to materialize feature set to feature store.
        :type materialization_settings: MaterializationSettings, optional
        :param stage: Stage of the asset
        :type stage: str, optional
        :param datastore_operations: operation to access workspace datastore
        :type datastore_operations: DatastoreOperations, optional
        :param tags: The feature set asset description
        :type tags: Dict(str, str)
        """

        with log_activity(_get_logger(), f"{PACKAGE_NAME}->FeatureSet.Init", ActivityType.PUBLICAPI):
            self._entities = entities
            self._specification = specification
            self._materialization_settings = materialization_settings
            self._stage = stage
            self.__feature_set_spec = None

            if self._specification:
                self.__feature_set_spec = FeatureSetSpec.from_config(
                    spec_path=self._specification.path, datastore_operations=datastore_operations
                )

            self.__offline_store = None
            self.__online_store = None
            self.__partition = None
            self.__is_registered = False
            self.__arm_id = None

            super().__init__(
                name=name,
                version=version,
                path=specification.path if specification else None,
                description=description,
                tags=tags,
                **kwargs,
            )

    def __repr__(self):
        info = OrderedDict()
        info["name"] = self.name.__repr__()
        info["version"] = self.version.__repr__()
        info["specification"] = self.specification.__repr__()
        info["source"] = self.source.__repr__()
        info["entities"] = [e.__repr__() for e in self.entities]
        info["features"] = [f.__repr__() for f in self.features]
        info["feature_transformation_code"] = self.feature_transformation_code.__repr__()
        info["timestamp_column"] = self.timestamp_column.__repr__()
        info["source_lookback"] = self.source_lookback.__repr__()
        info["temporal_join_lookback"] = self.temporal_join_lookback.__repr__()
        info["materialization_settings"] = self.materialization_settings.__repr__()
        info["description"] = self.description.__repr__()
        info["tags"] = self.tags.__repr__()
        info["stage"] = self.stage.__repr__()

        formatted_info = json.dumps(info, indent=2)
        return "FeatureSet\n{}".format(formatted_info)

    def __str__(self):
        return self.__repr__()

    def get_feature(self, name: str):
        if not isinstance(name, str):
            raise ValidationException(
                message=FEATURE_NAME_NOT_STRING_FEATURE_SET.format(type(name)),
                no_personal_data_message=FEATURE_NAME_NOT_STRING_FEATURE_SET,
                error_type=ValidationErrorType.INVALID_VALUE,
                error_category=ErrorCategory.USER_ERROR,
                target=ErrorTarget.GENERAL,
            )

        for feature in self.features:
            if feature.name == name:
                return feature

        raise ValidationException(
            message=FEATURE_NAME_NOT_FOUND_FEATURE_SET.format(name),
            no_personal_data_message=FEATURE_NAME_NOT_FOUND_FEATURE_SET,
            error_type=ValidationErrorType.INVALID_VALUE,
            error_category=ErrorCategory.USER_ERROR,
            target=ErrorTarget.GENERAL,
        )

    def __hash__(self):
        return hash(self.name)

    def _to_dict(self):
        d = {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "specification": {"path": self.specification.path},
            "entities": [e if isinstance(e, str) else f"azureml:{e.name}:{e.version}" for e in self.entities],
            "stage": self._stage,
        }
        if self.materialization_settings:
            d["materialization_settings"] = json.loads(
                json.dumps(
                    MaterializationSettingsSchema(unknown=EXCLUDE, context={BASE_PATH_CONTEXT_KEY: "./"}).dump(
                        self.materialization_settings
                    )
                )
            )

        return d

    @staticmethod
    def _load(config, config_file):
        from marshmallow import ValidationError

        context = {
            BASE_PATH_CONTEXT_KEY: Path(config_file).parent,
        }

        try:
            from azure.ai.ml._schema._feature_set import FeatureSetSchema

            config = FeatureSetSchema(context=context).load(config)
        except ValidationError as ex:
            raise ValueError(ex.messages) from ex

        return config

    @property
    def arm_id(self):
        return self.__arm_id

    @property
    def feature_store_guid(self):
        return self.__feature_store_guid

    @property
    def entities(self):
        return self._entities

    @property
    def features(self):
        def with_feature_set_ref(feature):
            feature.feature_set_reference = self
            return feature

        return [with_feature_set_ref(feature) for feature in self.__feature_set_spec.features]

    @property
    def timestamp_column(self):
        return self.__feature_set_spec.source.timestamp_column

    @property
    def stage(self):
        return self._stage

    @property
    def source(self):
        return self.__feature_set_spec.source

    @property
    def materialization_settings(self):
        return self._materialization_settings

    @property
    def feature_transformation_code(self):
        return self.__feature_set_spec.feature_transformation_code

    @property
    def source_lookback(self):
        return self.__feature_set_spec.source_lookback

    @property
    def temporal_join_lookback(self):
        return self.__feature_set_spec.temporal_join_lookback

    @property
    def specification(self):
        return self._specification

    @property
    def offline_store(self):
        return self.__offline_store

    @property
    def online_store(self):
        return self.__online_store

    @property
    def partition(self):
        return self.__partition

    def get_index_columns(self):
        return [
            Column(index_col.name, ColumnType[index_col.type.name.lower()])
            for e in self.entities
            for index_col in e.index_columns
        ]

    @monitor_with_activity(_get_logger(), f"{PACKAGE_NAME}->FeatureSet.ToSparkDataframe", ActivityType.PUBLICAPI)
    def to_spark_dataframe(
        self,
        *,
        featureWindowStartDateTime: datetime = None,
        featureWindowEndDateTime: datetime = None,
        features: List[str] = [],
        use_materialized_data: bool = True,
        **kwargs,
    ):
        """Display a featureset in spark dataframe format, after performing necessary transformation

        :param featureWindowStartDateTime: feature window start time
        :type featureWindowStartDateTime: datetime, optional, default: None
        :param featureWindowEndDateTime: feature window end time
        :type featureWindowEndDateTime: datetime, optional, default: None
        :param features: list of feature names to display
        :type features: List(str), optional, default: empty (include all features)
        :param direct_inject: flag to indicate whether to direct inject data from source
        :type direct_inject: bool, optional, default: False
        :param dedup: flag to indicate whether to deduplicate (multiple rows share the same join keys and event timestamp) when loading from source data
        :type dedup: bool, optional, default: False

        Returns:
            Dataframe: Spark Dataframe which can be used to show the results and do further operations.
        """

        try:
            self.validate()

            from azureml.featurestore._utils.spark_utils import _filter_dataframe
            from pyspark.sql import SparkSession

            # check spark session
            try:
                spark = SparkSession.builder.getOrCreate()
            except Exception:
                raise Exception("Fail to get spark session, please check if spark environment is set up.")

            timestamp_column, _ = self.get_timestamp_column()
            df = None

            # load from materialized data
            if use_materialized_data:
                # check materialization settings
                if not self.offline_store:
                    print(
                        "FeatureSet: {}, version: {}, offline store is not configured for its feature store..".format(
                            self.name, self.version
                        )
                    )
                    use_materialized_data = False
                if not self._materialization_settings:
                    print(
                        "FeatureSet: {}, version: {}, does not have materialization settings..".format(
                            self.name, self.version
                        )
                    )
                    use_materialized_data = False
                elif not self._materialization_settings.offline_enabled:
                    print(
                        "FeatureSet: {}, version: {}, does not have offline materialization enabled..".format(
                            self.name, self.version
                        )
                    )
                    use_materialized_data = False

            if use_materialized_data:
                index_columns = list(map(lambda i: i.name, self.get_index_columns()))

                df = self.offline_store.read_data(
                    feature_set=self,
                    feature_window_start_time=featureWindowStartDateTime,
                    feature_window_end_time=featureWindowEndDateTime,
                )

                if df:
                    print(
                        "FeatureSet: {}, version: {}, was materialized, load data from offline store: {}".format(
                            self.name, self.version, self.offline_store.target
                        )
                    )
                    if not features or len(features) == 0:
                        features = list(map(lambda f: f.name, self.features))

                    df = _filter_dataframe(
                        spark=spark,
                        df=df,
                        featureWindowStartDateTime=featureWindowStartDateTime,
                        featureWindowEndDateTime=featureWindowEndDateTime,
                        index_columns=index_columns,
                        timestamp_column=timestamp_column,
                        features=features,
                    )
                    return df
                else:
                    print(
                        "FeatureSet: {}, version: {}, was not materialized, please check offline store: {}".format(
                            self.name, self.version, self.offline_store.target
                        )
                    )
                    use_materialized_data = False
            # load from source data
            if not use_materialized_data:
                print("FeatureSet: {}, version: {} load data from source..".format(self.name, self.version))

                dedup = True if "dedup" in kwargs and kwargs["dedup"] is True else False
                df = self.__feature_set_spec.to_spark_dataframe(
                    featureWindowStartDateTime=featureWindowStartDateTime,
                    featureWindowEndDateTime=featureWindowEndDateTime,
                    features=features,
                    dedup=dedup,
                )

            return df

        except Exception as ex:
            if isinstance(ex, MlException):
                _get_logger().error(
                    f"{PACKAGE_NAME}->FeatureSet.ToSparkDataframe, {type(ex).__name__}: {ex.no_personal_data_message}"
                )
            else:
                _get_logger().error(f"{PACKAGE_NAME}->FeatureSet.ToSparkDataframe, {type(ex).__name__}: {ex}")

            log_and_raise_error(error=ex, debug=True)

    @classmethod
    @monitor_with_activity(_get_logger(), f"{PACKAGE_NAME}->FeatureSet.FromRestObject", ActivityType.INTERNALCALL)
    def _from_rest_object(
        cls,
        featureset_rest_object: FeaturesetVersion,
        ml_client: MLClient,
        datastore_operations: Optional[DatastoreOperations] = None,
    ) -> "FeatureSet":
        featureset_rest_object_details = featureset_rest_object.properties
        arm_id_object = get_arm_id_object_from_id(featureset_rest_object.id)
        featureset = FeatureSet(
            id=featureset_rest_object.id,
            name=arm_id_object.asset_name,
            version=arm_id_object.asset_version,
            description=featureset_rest_object_details.description,
            tags=featureset_rest_object_details.tags,
            properties=featureset_rest_object_details.properties,
            entities=featureset_rest_object_details.entities,
            materialization_settings=MaterializationSettings._from_rest_object(
                featureset_rest_object_details.materialization_settings
            ),
            specification=FeatureSetSpecification._from_rest_object(featureset_rest_object_details.specification),
            stage=featureset_rest_object_details.stage,
            datastore_operations=datastore_operations,
        )
        featureset.__is_registered = True
        featureset.__arm_id = arm_id_object

        # Temporary workaround to get the featurestore guid directly from ARM. When the featurestore response includes the featurestore GUID, remove this function.
        def get_feature_store_guid():
            workspace_response = requests.get(
                f"https://management.azure.com/subscriptions/{ml_client.subscription_id}/resourceGroups/{ml_client.resource_group_name}/providers/Microsoft.MachineLearningServices/workspaces/{ml_client.workspace_name}?api-version=2022-01-01-preview",
                headers={
                    "Authorization": f'Bearer {ml_client._credential.get_token("https://management.core.windows.net/.default").token}'
                },
            )
            workspace_response.raise_for_status()
            workspace_json = workspace_response.json()
            return workspace_json["properties"]["workspaceId"]

        featureset.__feature_store_guid = get_feature_store_guid()

        # partition strategy can be overriden by user in future
        from azureml.featurestore.offline_store.partition import TimestampPartition

        featureset.__partition = TimestampPartition(
            source_column=featureset.timestamp_column.name,
            partition_column=PARTITION_COLUMN,
            partition_strategy=TimestampPartition.PartitionStrategy.DAY,
        )

        featurestore = ml_client.feature_stores.get(name=ml_client.workspace_name)
        if featurestore:
            if featurestore.offline_store:
                from azureml.featurestore.contracts.offline_store import OfflineStoreFactory
                from azureml.featurestore.contracts.store_connection import OfflineStoreType

                featureset.__offline_store = OfflineStoreFactory.make_offline_store(
                    offline_store_type=OfflineStoreType[featurestore.offline_store.type],
                    offline_store_target=featurestore.offline_store.target,
                )
            if featurestore.online_store:
                from azureml.featurestore.contracts.online_store import OnlineStoreFactory
                from azureml.featurestore.contracts.store_connection import OnlineStoreType

                featureset.__online_store = OnlineStoreFactory.make_online_store(
                    online_store_type=OnlineStoreType[featurestore.online_store.type],
                    online_store_target=featurestore.online_store.target,
                )

        return featureset

    def validate(self):
        if not self.__is_registered:
            raise ValidationException(
                message=FEATURE_SET_NOT_REGISTERED,
                target=ErrorTarget.GENERAL,
                no_personal_data_message=FEATURE_SET_NOT_REGISTERED,
                error_category=ErrorCategory.USER_ERROR,
                error_type=ValidationErrorType.CANNOT_PARSE,
            )

    def get_timestamp_column(self):
        if not self.timestamp_column:
            # TODO: Suppport Non-timeseries data [prp2]
            raise ValidationException(
                message=MISSING_TIMESTAMP_COLUMN.format(self.name),
                no_personal_data_message=MISSING_TIMESTAMP_COLUMN,
                error_type=ValidationErrorType.MISSING_FIELD,
                error_category=ErrorCategory.USER_ERROR,
                target=ErrorTarget.GENERAL,
            )

        return self.timestamp_column.name, self.timestamp_column.format

    def _update_path(self, asset_artifact: ArtifactStorageInfo) -> None:
        regex = r"datastores\/(.+)"
        groups = re.search(regex, asset_artifact.datastore_arm_id)
        if groups:
            datastore_name = groups.group(1)
            self.path = SHORT_URI_FORMAT.format(datastore_name, asset_artifact.relative_path)
            self._specification.path = self.path
