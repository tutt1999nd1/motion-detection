from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'))


class KafkaProduce:
    def __init__(self, topic):
        self.topic = topic

    def producer(self, message):
        producer.send(self.topic, value=message)
