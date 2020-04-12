import sys

from confluent_kafka import Consumer
from confluent_kafka.cimpl import KafkaError, KafkaException

from db_persist import Mongo

mongo = Mongo('localhost', 27017, 'BikeDB', 'stolen_bikes')


class Consume:
    def __init__(self, topics, min_commit_count, persist_object):
        conf = {'bootstrap.servers': "localhost:9092",
                'group.id': "bike_theft",
                'default.topic.config': {'auto.offset.reset': 'smallest'},
                'on_commit': self.commit_completed}
        self.consumer = Consumer(conf)

        self.topics = topics
        self.min_commit_count = min_commit_count
        self.db = persist_object

    @staticmethod
    def commit_completed(err, partitions):
        if err:
            print(str(err))
        else:
            print("Committed partition offsets: " + str(partitions))

    def db_persist(self, msg):
        return self.db.insert(msg)

    def consume_loop(self):
        try:
            self.consumer.subscribe(self.topics)
            msg_count = 0
            while True:
                msg = self.consumer.poll(timeout=1.0)
                print(msg)
                if msg is None:
                    continue

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        sys.stderr.write(
                            '%% %s [%d] reached end at offset %d\n' % (msg.topic(), msg.partition(), msg.offset()))
                    elif msg.error():
                        raise KafkaException(msg.error())
                else:
                    decoded_msg = msg.value().decode("utf-8")
                    inserted_id = self.db_persist(decoded_msg)
                    msg_count += 1
                    if msg_count % self.min_commit_count == 0:
                        self.consumer.commit(asynchronous=False)
                    yield decoded_msg
        finally:
            self.consumer.close()


consume = Consume(['bike_theft'], 5, mongo)


