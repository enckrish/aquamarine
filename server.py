import collections
import uuid
from collections import deque
from concurrent import futures
from typing import Iterator, Dict, List

# GRPC Imports:
import grpc
from grpc_reflection.v1alpha import reflection

import pb.analyzer_pb2 as analyzer_pb2
import pb.analyzer_pb2_grpc as analyzer_pb2_grpc
import pb.analyzer_pb2_grpc as grpc_stub

DEBUG = True  # in prod, set to False
USE_LLM = True  # in prod, set to True
if not DEBUG or USE_LLM:
    from autogptpl import analyze_log

HistItemType = str


class DataStoreItem:
    def __init__(self, service: str, history_size: int):
        self.service = service
        self.history: deque[str] = collections.deque(maxlen=history_size)

    def get_history(self) -> List[HistItemType]:
        # TODO verify that self.buffer is returned in order
        return list(self.history)


class AnalyzerServicer(grpc_stub.AnalyzerServicer):
    data_store: Dict[str, DataStoreItem]

    def __init__(self):
        self.data_store = {}
        self.prompt_template = "### SERVICE: {service}\n\n### HISTORY:\n{history}\n\n###RECENT LOGS:\n{recent}"

    # Routes request to various nodes based on request parameters
    def route(self, req: analyzer_pb2.AnalyzerRequest_Type0):
        if not USE_LLM:
            # Dummy response
            return analyzer_pb2.AnalyzerResponse(
                id=req.id,
                rating=7,
                actionsInsights=["Do this", 'Not that'],
                citation=12345678
            )
        # In middleware, this will be changed to a gRPC call
        # target chosen based on req params, interface remains same
        return self.analyzer_wrapper_fn(req)

    # Calls Analyzer and performs necessary writes and transforms
    def analyzer_wrapper_fn(self, req: analyzer_pb2.AnalyzerRequest_Type0):
        meta = self.data_store[str(req.id.id)]
        history = meta.get_history()
        fmt_out, out = analyze_log(prompt_template=self.prompt_template,
                                   service=meta.service,
                                   history=history,
                                   recent=req.logs.logs
                                   )
        meta.history.appendleft(out)
        res = analyzer_pb2.AnalyzerResponse(
            id=req.id,
            rating=fmt_out['rating'],
            actionsInsights=fmt_out['actionable_insights'],
            review=fmt_out['review'],
            citation=fmt_out['citation']
        )

        return res

    def admin_setPromptTmpl(self, request: analyzer_pb2.String, context):
        self.prompt_template = request.str

    def init_type0(self, request: analyzer_pb2.InitRequest_Type0, context):
        service = request.service
        history_size = request.historySize

        unique_id = analyzer_pb2.UUID(id=str(uuid.uuid4()))
        self.data_store[str(unique_id.id)] = DataStoreItem(service, history_size)

        res = analyzer_pb2.InitResponse_Type0(id=unique_id)
        return res

    def analyzeLog_Type0(self, request_iterator: Iterator[analyzer_pb2.AnalyzerRequest_Type0], context):
        for req in request_iterator:
            analysis = self.route(req)
            yield analysis


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
