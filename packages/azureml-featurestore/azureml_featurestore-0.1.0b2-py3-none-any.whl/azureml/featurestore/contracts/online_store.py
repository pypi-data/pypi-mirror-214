# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from azureml.featurestore.contracts.store_connection import OnlineStoreType


class OnlineStore:
    def __init__(self, target: str, type: OnlineStoreType) -> None:
        self.target = target
        self.type = type


class OnlineStoreFactory:
    @staticmethod
    def make_online_store(online_store_type: OnlineStoreType, online_store_target: str) -> OnlineStore:
        return OnlineStore(target=online_store_target, type=online_store_type)
