#!/usr/bin/env python

from kafka import KafkaConsumer
import json


def decode(msg_value):
    event_dict = msg_value.decode("utf-8")
    return event_dict

consumer = KafkaConsumer('test.json',
                         bootstrap_servers=['localhost:9092'],
                         value_deserializer=lambda v: decode(v))
                         
try:
    print("Listening to the `test.json` topic")
    for msg in consumer:
        print(json.loads(json.dumps(msg.value)))
finally:
    consumer.close()