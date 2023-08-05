# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import os

__AZUREML_PRIVATE_FEATURES_ENVVAR = "AZURE_ML_CLI_PRIVATE_FEATURES_ENABLED"


def _is_private_preview_enabled():
    return os.getenv(__AZUREML_PRIVATE_FEATURES_ENVVAR) in ["True", "true", True]
