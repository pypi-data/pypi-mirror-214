# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from azureml.featurestore._version import VERSION

# constants
CREATE_TIMESTAMP_COLUMN = "create_timestamp"
SYS_CREATE_TIMESTAMP_COLUMN = "sys_create_timestamp"
SYS_UPDATE_TIMESTAMP_COLUMN = "sys_update_timestamp"

PARTITION_COLUMN = "partition"

MAXIMUM_MATERIALIZATION_RETRY_TIMES = 3

FEATURE_SET_SPEC_YAML_FILENAME = "FeatureSetSpec.yaml"
FEATURE_SET_SPEC_YAML_FILENAME_FALLBACK = "FeaturesetSpec.yaml"
FEATURE_SET_SPEC_FOLDERNAME = "spec"

FEATURE_RETRIEVAL_SPEC_YAML_FILENAME = "feature_retrieval_spec.yaml"

AZUREML_URI_PATTERNS = r"azureml://"
CLOUD_URI_PATTERNS = r"^https?://"
STORAGE_URI_PATTERNS = r"adl://|wasbs?://|abfss?://"

DATALAKE_URI_REGEX = r"([a-zA-Z0-9_\-]+)@([a-zA-Z0-9_\-]+).dfs.core.windows.net/([a-zA-Z0-9_/\-]+)"

PACKAGE_NAME = "{}/{}".format("featurestore", VERSION)

# metrics
NUMBER_OF_OFFLINE_MATERIALIZED_ROWS = "numberOfOfflineMaterializedRows"
NUMBER_OF_ONLINE_MATERIALIZED_ROWS = "numberOfOnlineMaterializedRows"
NUMBER_OF_SOURCE_ROWS = "numberOfSourceRows"

# offline query
QUERY_MODE_KEY = "query_mode"
QUERY_MODE_DEFAULT = "point_at_time"
QUERY_MODE_FEAST = "point_at_time_feast"

QUERY_APPLY_SOURCE_DELAY_KEY = "apply_source_delay"
QUERY_APPLY_TEMPORAL_JOIN_LOOKBACK_KEY = "apply_temporal_join_lookback"

COL_OBSERVATION_FEATURE_SET_UNIQUE_ROW_ID = "{fstore_guid}_{fset_name}_{fset_version}_entity_row_unique_id"

COL_OBSERVATION_ENTITY_TIMESTAMP = "entity_timestamp"

# online materialization
TIME_TO_LIVE = "time_to_live"
