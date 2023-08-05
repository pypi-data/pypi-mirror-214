# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------


def _get_lookup_key(featureset, row):
    prefix, suffix_column_name = _get_lookup_key_pattern(featureset)

    return _get_lookup_key_udf(prefix, suffix_column_name, row)


def _get_lookup_key_udf(prefix, suffix_column_names, row):
    suffix_parts = []

    for index_column in suffix_column_names:
        suffix_parts.append(index_column)
        suffix_parts.append(row[index_column])

    suffix = ":".join(suffix_parts)
    return f"{prefix}:{suffix}"

def _get_lookup_key_pattern(featureset):
    prefix = f"featurestore:{featureset.feature_store_guid}:featureset:{featureset.name}:version:{featureset.version}"

    suffix_column_names = []

    for entity in featureset.entities:
        for index_column in entity.index_columns:
            suffix_column_names.append(index_column.name)
    
    return prefix, suffix_column_names
