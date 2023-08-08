import collections
from typing import Iterator

import pb.analyzer_pb2 as analyzer_pb2
import pb.analyzer_pb2_grpc as analyzer_pb2_grpc
import pb.analyzer_pb2_grpc as grpc_stub
import grpc
from concurrent import futures
from grpc_reflection.v1alpha import reflection
from google.protobuf.json_format import MessageToJson, ParseDict
# from archive.llmc import run_llm
from archive.autogptpl import analys

class AnalyzerServicer(grpc_stub.AnalyzerServicer):
    def __init__(self):
        pass

    def llmPrompt(self, request: analyzer_pb2.Prompt, context):
        return analyzer_pb2.Prompt(pmt=analys(request.tmp, request.pmt))

    def analyzeLog(self, request_iterator: Iterator[analyzer_pb2.AnalyzerRequest], context):
        for req in request_iterator:
            print(req)
            # Dummy response, yield for every request
            yield analyzer_pb2.AnalyzerResponse(
                id=analyzer_pb2.UUID(id="some-uuid"),
                rating=7,
                review="Mildly dangerous",
                insight="Ignore bro",
                citation="Line 32"
            )


def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    analyzer_pb2_grpc.add_AnalyzerServicer_to_server(
        AnalyzerServicer(), server)
    service_names = (
        analyzer_pb2.DESCRIPTOR.services_by_name['Analyzer'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(service_names, server)
    server.add_insecure_port('[::]:' + port)
    print("Server started, listening on " + port)

    server.start()
    server.wait_for_termination()
