import os
import random
from collections import deque
from typing import List, Dict
import json
from pb import router_pb2 as pb
from confluent_kafka import Producer
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import dotenv

dotenv.load_dotenv()

DEBUG = True  # in prod, set to False
USE_LLM = False  # in prod, set to True
if not DEBUG or USE_LLM:
    from autogptpl import analyze_log


class DataStoreItem:
    def __init__(self, service: str, history_size: int):
        self.service = service
        self.history: deque[str] = deque(maxlen=history_size)

    def get_history(self) -> List[str]:
        return list(self.history)


def build_analysis_dict(stream_id: str, message_id: str, rating: int, action_insights: List[str], review: str,
                        citation: int):
    return {
        "stream_id": stream_id,
        "message_id": message_id,
        "rating": rating,
        "actions": action_insights,
        "review": review,
        "citation": citation
    }


class AnalyzerServicer:
    data_store: Dict[str, DataStoreItem]

    def __init__(self, _producer: Producer, analysis_store_topic: str):
        self.data_store = {}
        self.prompt_template = "### SERVICE: {service}\n\n### HISTORY:\n{history}\n\n###RECENT LOGS:\n{recent}"
        self.producer = _producer
        self.analysis_store_topic = analysis_store_topic

    # Internally routes request to various models based on request parameters
    def route(self, req: pb.AnalyzerRequest_Type0):
        res = None
        if not USE_LLM:
            # Dummy response
            res = build_analysis_dict(req.streamId, req.messageId, random.randint(0, 5), [], "", 1)
        elif req.streamId not in self.data_store:
            res = build_analysis_dict(req.streamId, req.messageId, 0, [], "", -1)
        else:
            res = self.analyzer_wrapper_fn(req)
        return res

    # Calls Analyzer and performs necessary writes and transforms
    def analyzer_wrapper_fn(self, req: pb.AnalyzerRequest_Type0):
        meta = self.data_store[str(req.streamId)]
        history = meta.get_history()
        fmt_out, out = analyze_log(prompt_template=self.prompt_template,
                                   service=meta.service,
                                   history=history,
                                   recent=req.logs
                                   )
        meta.history.appendleft(out)
        res = build_analysis_dict(
            req.streamId, req.messageId,
            fmt_out['rating'],
            fmt_out['actionable_insights'],
            fmt_out['review'], fmt_out['citation']
        )

        return res

    def admin_set_prompt_tmpl(self, request: str):
        self.prompt_template = request

    def init_type0(self, request: pb.InitRequest_Type0):
        self.data_store[request.streamId] = DataStoreItem(
            request.service, request.historySize
        )
        return True

    def analyze_log_type0(self, req: pb.AnalyzerRequest_Type0):
        if req.streamId not in self.data_store:
            return build_analysis_dict("", "", 0, [], "", -1)
        analysis = self.route(req)
        if analysis['citation'] == -1:  # Invalid Key
            return analysis
        self.producer.produce(
            topic=self.analysis_store_topic,
            key=self.data_store[req.streamId].service,
            value=json.dumps(analysis)
        )
        self.producer.flush()
        return analysis


def get_mongo_client() -> MongoClient:
    uri = f"mongodb+srv://ksengupta2911:{os.getenv('MONGO_PASSWORD')}@amberine-mumbai.g57yunl.mongodb.net/?retryWrites=true&w=majority"
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    # Send a ping to confirm a successful connection
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")

    return client
