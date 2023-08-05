# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import json
from collections import OrderedDict
from enum import Enum
from typing import Dict

from azureml.featurestore._utils.utils import _resolve_hdfs_path_from_storage_info
from azureml.featurestore.contracts import DateTimeOffset
from azureml.featurestore.contracts.timestamp_column import TimestampColumn

from azure.ai.ml.constants._common import BASE_PATH_CONTEXT_KEY
from azure.ai.ml.entities._assets import Artifact
from azure.ai.ml.entities._assets._artifacts.artifact import ArtifactStorageInfo
from azure.core import CaseInsensitiveEnumMeta


class SourceType(Enum, metaclass=CaseInsensitiveEnumMeta):
    """Represents feature source type"""

    MLTABLE = "mltable"
    CSV = "csv"
    PARQUET = "parquet"
    DELTATABLE = "deltaTable"

    def __str__(self):
        return self.value


class FeatureSource(Artifact):
    """A featurestore source
    :param type: The source type
    :type type: str, required
    :param path: The source data path
    :type path: str, required
    :param timestamp_column: Timestamp column for this feature set
    :type timestamp_column: TimestampColumn, required
    :param source_delay: The source delay
    :type source_delay: DateTimeOffset, optional"""

    def __init__(
        self,
        *,
        type: SourceType,
        path: str,
        timestamp_column: TimestampColumn,
        source_delay: DateTimeOffset = None,
        **kwargs
    ):
        self.type = type
        self.timestamp_column = timestamp_column
        self.source_delay = source_delay

        super().__init__(
            path=path,
            **kwargs,
        )

    def __repr__(self):
        info = OrderedDict()

        info["type"] = self.type
        info["path"] = self.path
        info["timestamp_column"] = self.timestamp_column.__repr__()
        info["source_delay"] = self.source_delay.__repr__()
        formatted_info = ", ".join(["{}: {}".format(k, v) for k, v in info.items()])
        return "FeatureSource({})".format(formatted_info)

    def __str__(self):
        return self.__repr__()

    def _update_path(self, asset_artifact: ArtifactStorageInfo) -> None:
        # Workaround for cross-workspace data access
        hdfs_path = _resolve_hdfs_path_from_storage_info(asset_artifact)
        self.path = hdfs_path

    def _load(self):
        pass

    def _to_dict(self) -> Dict:
        from azureml.featurestore.schema.feature_set_schema import Source
        from marshmallow import EXCLUDE

        return json.loads(json.dumps(Source(unknown=EXCLUDE, context={BASE_PATH_CONTEXT_KEY: "./"}).dump(self)))
