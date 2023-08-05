# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import json
import sys
import threading

import pyarrow
import pyarrow.flight
from azureml.featurestore.online import OnlineFeatureGetter

from azure.core.credentials import AccessToken


class AuthTokenCredential(object):
    def __init__(self, token_dict):
        self.tokens = token_dict

    def get_token(self, scope):
        token = self.tokens[scope]
        return AccessToken(token["token"], token["expires_on"])


class FlightFeatureRetrievalServer(pyarrow.flight.FlightServerBase):
    def __init__(self, location, credential, feature_uris):
        super(FlightFeatureRetrievalServer, self).__init__(location)
        self.online_feature_getter = OnlineFeatureGetter(credential, feature_uris)

    def do_exchange(self, context, descriptor, reader, writer):
        """Write data to a flight.
        Applications should override this method to implement their
        own behavior. The default method raises a NotImplementedError.
        Parameters
        ----------
        context : ServerCallContext
            Common contextual information.
        descriptor : FlightDescriptor
            The descriptor for the flight provided by the client.
        reader : MetadataRecordBatchReader
            A reader for data uploaded by the client.
        writer : MetadataRecordBatchWriter
            A writer to send responses to the client.
        """
        # Get feature list from descriptor
        scenario = descriptor.path[0].decode("utf-8")

        if scenario == "online":
            feature_getter = self.online_feature_getter.get_online_features
        elif scenario.startswith("offline:"):
            raise NotImplementedError(f"Offline feature data retrieval over grpc is not yet supported.")
        else:
            raise NotImplementedError(f"Unsupported scenario: {scenario}")

        feature_uris = [path.decode("utf-8") for path in descriptor.path[1:]]

        # Get observations dataframe from request
        observation_df = reader.read_pandas()
        features_df = feature_getter(feature_uris, observation_df)

        writer.begin(pyarrow.Schema.from_pandas(features_df))
        writer.write_table(pyarrow.Table.from_pandas(features_df))
        writer.close()


def sentinel(server):
    # Wait as long as stdin is open.
    for line in sys.stdin:
        pass

    # stdin was closed - the parent process is likely dead.
    sys.stdout.flush()
    sys.stderr.flush()
    server.shutdown()


def main(location, credential, feature_uris):
    server = FlightFeatureRetrievalServer(location, credential, feature_uris)
    threading.Thread(target=sentinel, args=(server,)).start()
    server.serve()


if __name__ == "__main__":
    # Read initialization params from stdin
    initialization_params = json.loads(sys.stdin.readline())
    location = initialization_params["location"]
    feature_uris = initialization_params["features"]
    credential = AuthTokenCredential(initialization_params["tokens"])

    main(location, credential, feature_uris)
