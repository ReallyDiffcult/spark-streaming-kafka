#!/usr/bin/env python

from kafka import KafkaConsumer
import avro.schema
from avro.io import BinaryDecoder, DatumReader
import io
import os


consumer = KafkaConsumer('test.avro',
                         bootstrap_servers=['localhost:9092'])
                         
cwd = os.getcwd()
schema_path = os.path.join(cwd, 'avro/schemas/user.avsc')
schema = avro.schema.Parse(open(schema_path).read())
                         
try:
    print("Listening to the `test.avro` topic")
    for msg in consumer:
        bytes_reader = io.BytesIO(msg.value)
        decoder = BinaryDecoder(bytes_reader)
        reader = DatumReader(schema)
        user = reader.read(decoder)
        print(user)
finally:
    consumer.close()