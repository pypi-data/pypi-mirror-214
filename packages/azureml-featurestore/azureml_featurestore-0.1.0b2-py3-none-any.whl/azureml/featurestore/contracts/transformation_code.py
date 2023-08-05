# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------


import os

from azureml.featurestore._utils.utils import (
    PathType,
    _download_file,
    _parse_path_format,
    _strip_local_path,
    copy_rename_and_zip,
)

from azure.ai.ml.exceptions import ErrorCategory, ErrorTarget, ValidationErrorType, ValidationException
from azure.ai.ml.operations import DatastoreOperations


class TransformationCode(object):
    """Feature transformation code representation
    :param type: The source type
    :type type: str, required
    :param path: The source data path
    :type path: str, required"""

    def __init__(self, *, path, transformer_class):
        self.path = path
        self.transformer_class = transformer_class

    def __repr__(self):
        return f"TransformationCode(Path={self.path},TransformerClass={self.transformer_class})"

    def __str__(self):
        return self.__repr__()

    def _to_dict(self):
        return {"path": self.path, "transformer_class": self.transformer_class}

    def _patch_zip(self, spec_folder_path: str = None, datastore_operations: DatastoreOperations = None) -> str:
        if spec_folder_path:
            code_path = _strip_local_path(self.path)
            code_path_type, code_path = _parse_path_format(code_path)

            if code_path_type == PathType.cloud:
                msg = "Transformation code must be relative to spec_folder_path {}. Found: {}"
                raise ValidationException(
                    message=msg.format(spec_folder_path, code_path),
                    no_personal_data_message="Transformation code must be relative to spec_folder_path",
                    error_type=ValidationErrorType.INVALID_VALUE,
                    error_category=ErrorCategory.USER_ERROR,
                    target=ErrorTarget.GENERAL,
                )

            code_path = os.path.join(spec_folder_path, code_path)
        else:
            code_path = self.path

        path_type, code_path = _parse_path_format(code_path)
        if path_type != PathType.local:
            code_path = _download_file(path=code_path, path_type=path_type, datastore_operations=datastore_operations)

        # Put code in a uuid() folder and zip so that sc can import script without collision
        code_zip = copy_rename_and_zip(code_path)
        return code_zip
