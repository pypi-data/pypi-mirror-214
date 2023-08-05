# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import retriever_pb2 as retriever__pb2


class RetrievingServiceStub(object):
    """*
    Service to process and retrieve documents
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetRetrievers = channel.unary_unary(
                '/retrieve.RetrievingService/GetRetrievers',
                request_serializer=retriever__pb2.GetRetrieversRequest.SerializeToString,
                response_deserializer=retriever__pb2.GetRetrieversResponse.FromString,
                )
        self.Retrieve = channel.unary_unary(
                '/retrieve.RetrievingService/Retrieve',
                request_serializer=retriever__pb2.RetrieveRequest.SerializeToString,
                response_deserializer=retriever__pb2.RetrieveResponse.FromString,
                )


class RetrievingServiceServicer(object):
    """*
    Service to process and retrieve documents
    """

    def GetRetrievers(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Retrieve(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RetrievingServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetRetrievers': grpc.unary_unary_rpc_method_handler(
                    servicer.GetRetrievers,
                    request_deserializer=retriever__pb2.GetRetrieversRequest.FromString,
                    response_serializer=retriever__pb2.GetRetrieversResponse.SerializeToString,
            ),
            'Retrieve': grpc.unary_unary_rpc_method_handler(
                    servicer.Retrieve,
                    request_deserializer=retriever__pb2.RetrieveRequest.FromString,
                    response_serializer=retriever__pb2.RetrieveResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'retrieve.RetrievingService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class RetrievingService(object):
    """*
    Service to process and retrieve documents
    """

    @staticmethod
    def GetRetrievers(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/retrieve.RetrievingService/GetRetrievers',
            retriever__pb2.GetRetrieversRequest.SerializeToString,
            retriever__pb2.GetRetrieversResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Retrieve(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/retrieve.RetrievingService/Retrieve',
            retriever__pb2.RetrieveRequest.SerializeToString,
            retriever__pb2.RetrieveResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
