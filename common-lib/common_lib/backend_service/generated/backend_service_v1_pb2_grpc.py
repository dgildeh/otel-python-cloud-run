# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from common_lib.backend_service.generated import service_types_v1_pb2 as service__types__v1__pb2


class BackendServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Greet = channel.unary_unary(
                '/backend_service.v1.BackendService/Greet',
                request_serializer=service__types__v1__pb2.GreetRequest.SerializeToString,
                response_deserializer=service__types__v1__pb2.GreetResult.FromString,
                )


class BackendServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Greet(self, request, context):
        """
        A simple gRPC method that generates some logs and a trace span.

        Send a name and get a simple `Hello {name}` back
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_BackendServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Greet': grpc.unary_unary_rpc_method_handler(
                    servicer.Greet,
                    request_deserializer=service__types__v1__pb2.GreetRequest.FromString,
                    response_serializer=service__types__v1__pb2.GreetResult.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'backend_service.v1.BackendService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class BackendService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Greet(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/backend_service.v1.BackendService/Greet',
            service__types__v1__pb2.GreetRequest.SerializeToString,
            service__types__v1__pb2.GreetResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
