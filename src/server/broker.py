from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import Producer
import socket


class Broker:
    def __init__(self, topics):
        conf = {'bootstrap.servers': "localhost:9092",
                'client.id': socket.gethostname()}

        self.producer = Producer(conf)

        admin = AdminClient(conf)
        self.create_topics(admin, topics)

    @staticmethod
    def create_topics(admin, topics):
        """ Create topics """
        new_topics = [NewTopic(topic, num_partitions=1, replication_factor=1) for topic in topics]
        fs = admin.create_topics(new_topics)
        for topic, f in fs.items():
            try:
                f.result()
                print("Topic {} created".format(topic))
            except Exception as e:
                print("Failed to create topic {}: {}".format(topic, e))


producer = Broker(['bike_theft']).producer
