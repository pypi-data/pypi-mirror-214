# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import datetime
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from azureml.featurestore._feature_set import FeatureSet
from azureml.featurestore.contracts.store_connection import OfflineStoreType

if TYPE_CHECKING:
    from pyspark.sql import DataFrame


class OfflineStore(ABC):
    def __init__(self, *, target: str) -> None:
        self.target = target

    @abstractmethod
    def read_data(
        self,
        featureset: FeatureSet,
        feature_window_start_time: datetime = None,
        feature_window_end_time: datetime = None,
    ) -> "DataFrame":
        pass

    @abstractmethod
    def write_data(self, featureset: FeatureSet, df: "DataFrame", upsert: bool = True) -> None:
        pass

    @abstractmethod
    def validate_data(
        self,
        featureset: FeatureSet,
        feature_window_start_time: datetime = None,
        feature_window_end_time: datetime = None,
    ) -> "DataFrame":
        pass

    def get_spark_session(self):
        from pyspark.sql import SparkSession

        try:
            self.spark = SparkSession.builder.getOrCreate()
        except Exception:
            raise Exception("Fail to get spark session, please check if spark environment is set up.")


class OfflineStoreFactory:
    @staticmethod
    def make_offline_store(offline_store_type: OfflineStoreType, offline_store_target: str) -> OfflineStore:
        if offline_store_type == OfflineStoreType.AZURE_DATA_LAKE_GEN2:
            from azureml.featurestore.offline_store.azure_data_lake_offline_store import AzureDataLakeOfflineStore

            return AzureDataLakeOfflineStore(target=offline_store_target)
        else:
            raise NotImplementedError(f"Offline store type:{offline_store_type.name} is not supported")
