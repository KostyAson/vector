# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from cloudapi.output.yandex.cloud.ai.stt.v3 import stt_pb2 as yandex_dot_cloud_dot_ai_dot_stt_dot_v3_dot_stt__pb2
from cloudapi.output.yandex.cloud.ai.stt.v3 import stt_service_pb2 as yandex_dot_cloud_dot_ai_dot_stt_dot_v3_dot_stt__service__pb2
from cloudapi.output.yandex.cloud.operation import operation_pb2 as yandex_dot_cloud_dot_operation_dot_operation__pb2


class RecognizerStub(object):
    """A set of methods for voice recognition.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.RecognizeStreaming = channel.stream_stream(
                '/speechkit.stt.v3.Recognizer/RecognizeStreaming',
                request_serializer=yandex_dot_cloud_dot_ai_dot_stt_dot_v3_dot_stt__pb2.StreamingRequest.SerializeToString,
                response_deserializer=yandex_dot_cloud_dot_ai_dot_stt_dot_v3_dot_stt__pb2.StreamingResponse.FromString,
                )


class RecognizerServicer(object):
    """A set of methods for voice recognition.
    """

    def RecognizeStreaming(self, request_iterator, context):
        """Expects audio in real-time
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RecognizerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'RecognizeStreaming': grpc.stream_stream_rpc_method_handler(
                    servicer.RecognizeStreaming,
                    request_deserializer=yandex_dot_cloud_dot_ai_dot_stt_dot_v3_dot_stt__pb2.StreamingRequest.FromString,
                    response_serializer=yandex_dot_cloud_dot_ai_dot_stt_dot_v3_dot_stt__pb2.StreamingResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'speechkit.stt.v3.Recognizer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Recognizer(object):
    """A set of methods for voice recognition.
    """

    @staticmethod
    def RecognizeStreaming(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/speechkit.stt.v3.Recognizer/RecognizeStreaming',
            yandex_dot_cloud_dot_ai_dot_stt_dot_v3_dot_stt__pb2.StreamingRequest.SerializeToString,
            yandex_dot_cloud_dot_ai_dot_stt_dot_v3_dot_stt__pb2.StreamingResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class AsyncRecognizerStub(object):
    """A set of methods for async voice recognition.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.RecognizeFile = channel.unary_unary(
                '/speechkit.stt.v3.AsyncRecognizer/RecognizeFile',
                request_serializer=yandex_dot_cloud_dot_ai_dot_stt_dot_v3_dot_stt__pb2.RecognizeFileRequest.SerializeToString,
                response_deserializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.FromString,
                )
        self.GetRecognition = channel.unary_stream(
                '/speechkit.stt.v3.AsyncRecognizer/GetRecognition',
                request_serializer=yandex_dot_cloud_dot_ai_dot_stt_dot_v3_dot_stt__service__pb2.GetRecognitionRequest.SerializeToString,
                response_deserializer=yandex_dot_cloud_dot_ai_dot_stt_dot_v3_dot_stt__pb2.StreamingResponse.FromString,
                )


class AsyncRecognizerServicer(object):
    """A set of methods for async voice recognition.
    """

    def RecognizeFile(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetRecognition(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AsyncRecognizerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'RecognizeFile': grpc.unary_unary_rpc_method_handler(
                    servicer.RecognizeFile,
                    request_deserializer=yandex_dot_cloud_dot_ai_dot_stt_dot_v3_dot_stt__pb2.RecognizeFileRequest.FromString,
                    response_serializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.SerializeToString,
            ),
            'GetRecognition': grpc.unary_stream_rpc_method_handler(
                    servicer.GetRecognition,
                    request_deserializer=yandex_dot_cloud_dot_ai_dot_stt_dot_v3_dot_stt__service__pb2.GetRecognitionRequest.FromString,
                    response_serializer=yandex_dot_cloud_dot_ai_dot_stt_dot_v3_dot_stt__pb2.StreamingResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'speechkit.stt.v3.AsyncRecognizer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class AsyncRecognizer(object):
    """A set of methods for async voice recognition.
    """

    @staticmethod
    def RecognizeFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/speechkit.stt.v3.AsyncRecognizer/RecognizeFile',
            yandex_dot_cloud_dot_ai_dot_stt_dot_v3_dot_stt__pb2.RecognizeFileRequest.SerializeToString,
            yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetRecognition(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/speechkit.stt.v3.AsyncRecognizer/GetRecognition',
            yandex_dot_cloud_dot_ai_dot_stt_dot_v3_dot_stt__service__pb2.GetRecognitionRequest.SerializeToString,
            yandex_dot_cloud_dot_ai_dot_stt_dot_v3_dot_stt__pb2.StreamingResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
