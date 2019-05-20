#!/usr/bin/env python

from kafka import KafkaProducer
import avro.schema
from avro.io import DatumWriter, BinaryEncoder
import io
import random
from time import sleep
import os

producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

cwd = os.getcwd()
schema_path = os.path.join(cwd, 'avro/schemas/user.avsc')
schema = avro.schema.Parse(open(schema_path).read())

i = 0
while True:
    print(f"Sending message {i}")
    try:
        writer = DatumWriter(schema)
        bytes_writer = io.BytesIO()
        encoder = BinaryEncoder(bytes_writer)
        writer.write({
            "name": "Robert",
            "favorite_number": i,
            "favorite_color": "blue"
        }, encoder)
        raw_bytes = bytes_writer.getvalue()
        producer.send('test.avro', raw_bytes)
        sleep(1)
        i += 1
    except Exception as e:
        print(f"Error: {e}")