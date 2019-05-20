#!/usr/bin/env python

from kafka import KafkaProducer
import json
from time import sleep

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

i = 0
while True:
    print(f"Sending message {i}")
    try:
        producer.send('test.json', { "message": "This is a test message", "number": i})
        sleep(1)
        i += 1
    except Exception as e:
        print(f"Error: {e}")