# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""

import grpc

from chalk._gen.chalk.aggregate.v1 import service_pb2 as chalk_dot_aggregate_dot_v1_dot_service__pb2
from chalk._gen.chalk.common.v1 import online_query_pb2 as chalk_dot_common_dot_v1_dot_online__query__pb2
from chalk._gen.chalk.common.v1 import upload_features_pb2 as chalk_dot_common_dot_v1_dot_upload__features__pb2
from chalk._gen.chalk.engine.v1 import query_server_pb2 as chalk_dot_engine_dot_v1_dot_query__server__pb2


class QueryServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Ping = channel.unary_unary(
            "/chalk.engine.v1.QueryService/Ping",
            request_serializer=chalk_dot_engine_dot_v1_dot_query__server__pb2.PingRequest.SerializeToString,
            response_deserializer=chalk_dot_engine_dot_v1_dot_query__server__pb2.PingResponse.FromString,
        )
        self.OnlineQuery = channel.unary_unary(
            "/chalk.engine.v1.QueryService/OnlineQuery",
            request_serializer=chalk_dot_common_dot_v1_dot_online__query__pb2.OnlineQueryRequest.SerializeToString,
            response_deserializer=chalk_dot_common_dot_v1_dot_online__query__pb2.OnlineQueryResponse.FromString,
        )
        self.OnlineQueryBulk = channel.unary_unary(
            "/chalk.engine.v1.QueryService/OnlineQueryBulk",
            request_serializer=chalk_dot_common_dot_v1_dot_online__query__pb2.OnlineQueryBulkRequest.SerializeToString,
            response_deserializer=chalk_dot_common_dot_v1_dot_online__query__pb2.OnlineQueryBulkResponse.FromString,
        )
        self.OnlineQueryMulti = channel.unary_unary(
            "/chalk.engine.v1.QueryService/OnlineQueryMulti",
            request_serializer=chalk_dot_common_dot_v1_dot_online__query__pb2.OnlineQueryMultiRequest.SerializeToString,
            response_deserializer=chalk_dot_common_dot_v1_dot_online__query__pb2.OnlineQueryMultiResponse.FromString,
        )
        self.UploadFeaturesBulk = channel.unary_unary(
            "/chalk.engine.v1.QueryService/UploadFeaturesBulk",
            request_serializer=chalk_dot_common_dot_v1_dot_online__query__pb2.UploadFeaturesBulkRequest.SerializeToString,
            response_deserializer=chalk_dot_common_dot_v1_dot_online__query__pb2.UploadFeaturesBulkResponse.FromString,
        )
        self.UploadFeatures = channel.unary_unary(
            "/chalk.engine.v1.QueryService/UploadFeatures",
            request_serializer=chalk_dot_common_dot_v1_dot_upload__features__pb2.UploadFeaturesRequest.SerializeToString,
            response_deserializer=chalk_dot_common_dot_v1_dot_upload__features__pb2.UploadFeaturesResponse.FromString,
        )
        self.PlanAggregateBackfill = channel.unary_unary(
            "/chalk.engine.v1.QueryService/PlanAggregateBackfill",
            request_serializer=chalk_dot_aggregate_dot_v1_dot_service__pb2.PlanAggregateBackfillRequest.SerializeToString,
            response_deserializer=chalk_dot_aggregate_dot_v1_dot_service__pb2.PlanAggregateBackfillResponse.FromString,
        )
        self.GetAggregates = channel.unary_unary(
            "/chalk.engine.v1.QueryService/GetAggregates",
            request_serializer=chalk_dot_aggregate_dot_v1_dot_service__pb2.GetAggregatesRequest.SerializeToString,
            response_deserializer=chalk_dot_aggregate_dot_v1_dot_service__pb2.GetAggregatesResponse.FromString,
        )


class QueryServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Ping(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def OnlineQuery(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def OnlineQueryBulk(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def OnlineQueryMulti(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def UploadFeaturesBulk(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def UploadFeatures(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def PlanAggregateBackfill(self, request, context):
        """PlanAggregateBackfill determines the estimated resources needed to backfill
        an aggregate.

        This method is a duplicate of the PlanAggregateBackfill method
        in the query_server.proto file. We should remove the query_server.proto method
        and move that request to this service instead.
        buf:lint:ignore RPC_REQUEST_RESPONSE_UNIQUE
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def GetAggregates(self, request, context):
        """This method is a duplicate of the PlanAggregateBackfill method
        in the query_server.proto file. We should remove the query_server.proto method
        and move that request to this service instead.
        buf:lint:ignore RPC_REQUEST_RESPONSE_UNIQUE
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_QueryServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "Ping": grpc.unary_unary_rpc_method_handler(
            servicer.Ping,
            request_deserializer=chalk_dot_engine_dot_v1_dot_query__server__pb2.PingRequest.FromString,
            response_serializer=chalk_dot_engine_dot_v1_dot_query__server__pb2.PingResponse.SerializeToString,
        ),
        "OnlineQuery": grpc.unary_unary_rpc_method_handler(
            servicer.OnlineQuery,
            request_deserializer=chalk_dot_common_dot_v1_dot_online__query__pb2.OnlineQueryRequest.FromString,
            response_serializer=chalk_dot_common_dot_v1_dot_online__query__pb2.OnlineQueryResponse.SerializeToString,
        ),
        "OnlineQueryBulk": grpc.unary_unary_rpc_method_handler(
            servicer.OnlineQueryBulk,
            request_deserializer=chalk_dot_common_dot_v1_dot_online__query__pb2.OnlineQueryBulkRequest.FromString,
            response_serializer=chalk_dot_common_dot_v1_dot_online__query__pb2.OnlineQueryBulkResponse.SerializeToString,
        ),
        "OnlineQueryMulti": grpc.unary_unary_rpc_method_handler(
            servicer.OnlineQueryMulti,
            request_deserializer=chalk_dot_common_dot_v1_dot_online__query__pb2.OnlineQueryMultiRequest.FromString,
            response_serializer=chalk_dot_common_dot_v1_dot_online__query__pb2.OnlineQueryMultiResponse.SerializeToString,
        ),
        "UploadFeaturesBulk": grpc.unary_unary_rpc_method_handler(
            servicer.UploadFeaturesBulk,
            request_deserializer=chalk_dot_common_dot_v1_dot_online__query__pb2.UploadFeaturesBulkRequest.FromString,
            response_serializer=chalk_dot_common_dot_v1_dot_online__query__pb2.UploadFeaturesBulkResponse.SerializeToString,
        ),
        "UploadFeatures": grpc.unary_unary_rpc_method_handler(
            servicer.UploadFeatures,
            request_deserializer=chalk_dot_common_dot_v1_dot_upload__features__pb2.UploadFeaturesRequest.FromString,
            response_serializer=chalk_dot_common_dot_v1_dot_upload__features__pb2.UploadFeaturesResponse.SerializeToString,
        ),
        "PlanAggregateBackfill": grpc.unary_unary_rpc_method_handler(
            servicer.PlanAggregateBackfill,
            request_deserializer=chalk_dot_aggregate_dot_v1_dot_service__pb2.PlanAggregateBackfillRequest.FromString,
            response_serializer=chalk_dot_aggregate_dot_v1_dot_service__pb2.PlanAggregateBackfillResponse.SerializeToString,
        ),
        "GetAggregates": grpc.unary_unary_rpc_method_handler(
            servicer.GetAggregates,
            request_deserializer=chalk_dot_aggregate_dot_v1_dot_service__pb2.GetAggregatesRequest.FromString,
            response_serializer=chalk_dot_aggregate_dot_v1_dot_service__pb2.GetAggregatesResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler("chalk.engine.v1.QueryService", rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class QueryService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Ping(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/chalk.engine.v1.QueryService/Ping",
            chalk_dot_engine_dot_v1_dot_query__server__pb2.PingRequest.SerializeToString,
            chalk_dot_engine_dot_v1_dot_query__server__pb2.PingResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def OnlineQuery(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/chalk.engine.v1.QueryService/OnlineQuery",
            chalk_dot_common_dot_v1_dot_online__query__pb2.OnlineQueryRequest.SerializeToString,
            chalk_dot_common_dot_v1_dot_online__query__pb2.OnlineQueryResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def OnlineQueryBulk(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/chalk.engine.v1.QueryService/OnlineQueryBulk",
            chalk_dot_common_dot_v1_dot_online__query__pb2.OnlineQueryBulkRequest.SerializeToString,
            chalk_dot_common_dot_v1_dot_online__query__pb2.OnlineQueryBulkResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def OnlineQueryMulti(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/chalk.engine.v1.QueryService/OnlineQueryMulti",
            chalk_dot_common_dot_v1_dot_online__query__pb2.OnlineQueryMultiRequest.SerializeToString,
            chalk_dot_common_dot_v1_dot_online__query__pb2.OnlineQueryMultiResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def UploadFeaturesBulk(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/chalk.engine.v1.QueryService/UploadFeaturesBulk",
            chalk_dot_common_dot_v1_dot_online__query__pb2.UploadFeaturesBulkRequest.SerializeToString,
            chalk_dot_common_dot_v1_dot_online__query__pb2.UploadFeaturesBulkResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def UploadFeatures(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/chalk.engine.v1.QueryService/UploadFeatures",
            chalk_dot_common_dot_v1_dot_upload__features__pb2.UploadFeaturesRequest.SerializeToString,
            chalk_dot_common_dot_v1_dot_upload__features__pb2.UploadFeaturesResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def PlanAggregateBackfill(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/chalk.engine.v1.QueryService/PlanAggregateBackfill",
            chalk_dot_aggregate_dot_v1_dot_service__pb2.PlanAggregateBackfillRequest.SerializeToString,
            chalk_dot_aggregate_dot_v1_dot_service__pb2.PlanAggregateBackfillResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def GetAggregates(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/chalk.engine.v1.QueryService/GetAggregates",
            chalk_dot_aggregate_dot_v1_dot_service__pb2.GetAggregatesRequest.SerializeToString,
            chalk_dot_aggregate_dot_v1_dot_service__pb2.GetAggregatesResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
