# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
# isort: skip_file

__path__ = __import__("pkgutil").extend_path(__path__, __name__)  # type: ignore

from .feature_set_spec import FeatureSetSpec, create_feature_set_spec
from .feature_store_client import FeatureStoreClient, get_offline_features

__all__ = [
    "create_feature_set_spec",
    "get_offline_features",
    "FeatureSetSpec",
    "FeatureStoreClient",
]

from azureml.featurestore._utils._preview_method import _is_private_preview_enabled

if _is_private_preview_enabled():
    from .feature_store_client import init_online_lookup, shutdown_online_lookup, get_online_features

    __all__ += [
        "init_online_lookup",
        "shutdown_online_lookup",
        "get_online_features",
    ]
