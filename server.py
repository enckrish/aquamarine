import json
import sys

import leader
from pb import router_pb2 as pb
from confluent_kafka import Producer, Consumer, KafkaError, KafkaException, Message
import socket

from utils import AnalyzerServicer

bootstrap_servers = "localhost:9092"
kafka_conf = {
    'bootstrap.servers': bootstrap_servers,
    'client.id': socket.gethostname(),
}
kafka_consumer_conf = {
    'bootstrap.servers': bootstrap_servers,
    'group.id': 'analyzer',
    'auto.offset.reset': 'largest'
}
analysisStoreTopic = "topic.log.analysis.result.1"
analysisRequestStoreTopic = "topic.log.requests.analysis.1"

producer = Producer(kafka_conf)
consumer = Consumer(kafka_consumer_conf)
servicer = AnalyzerServicer(producer, analysis_store_topic=analysisStoreTopic)

running = True


# Listen to kafka events here
def listen():
    basic_consume_loop(consumer)


def basic_consume_loop(consumer_: Consumer):
    global running
    try:
        consumer_.subscribe([analysisRequestStoreTopic, analysisStoreTopic])
        while running:
            msg = consumer_.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                msg_process(msg)
    finally:
        consumer_.close()


def shutdown():
    global running
    running = False


# If LLM not running citation -1 returned, as error, not want that, only return that if no key found
def msg_process(msg: Message):
    topic = msg.topic()
    decoded = msg.value().decode("utf-8")
    decoded_pb = json.loads(decoded)

    # print("Topic:", topic, decoded_pb)
    if topic == analysisRequestStoreTopic:
        init_msg = 'messageId' not in decoded_pb
        if init_msg:
            print("Init message:", decoded_pb['streamId'])
            if not leader.is_target(decoded_pb['service']):
                return
            data = pb.InitRequest_Type0(
                streamId=decoded_pb['streamId'],
                service=decoded_pb['service'],
                historySize=decoded_pb['historySize']
            )
            servicer.init_type0(data)
        else:
            data = pb.AnalyzerRequest_Type0(
                streamId=decoded_pb['streamId'],
                messageId=decoded_pb['messageId'],
                logs=decoded_pb['logs'],
            )
            servicer.analyze_log_type0(data)
    else:
        print("Produced:", topic, decoded)
