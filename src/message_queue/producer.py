from server.broker import producer


def acknowledge(err, msg):
    if err is not None:
        print(f'Failed to deliver message: {msg.value().decode("utf-8")}, {str(err)}')
    else:
        print(f'Message produced: {msg.value().decode("utf-8")}')


def produce_assignment(topic, value, key=None, callback=acknowledge):
    producer.produce(topic, key=key, value=value, callback=callback)
    producer.poll(1)


