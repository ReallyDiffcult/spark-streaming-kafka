#!/usr/bin/env python

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from fastavro import schemaless_reader, parse_schema
import io
import os
import json

os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-avro_2.11:2.4.0,org.apache.spark:spark-sql-kafka-0-10_2.11:2.1.0,org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.2 pyspark-shell'

cwd = os.getcwd()
schema_path = os.path.join(cwd, 'avro/schemas/user.avsc')
with open(schema_path, 'r') as f:
    data = json.load(f)
schema = parse_schema(data)

def decoder(msg):
    bytes_reader = io.BytesIO(msg)
    bytes_reader.seek(0)
    user = schemaless_reader(bytes_reader, schema)
    return user

# Create a spark context
sc = SparkContext(appName="SparkStreamingTest")
ssc = StreamingContext(sc, 5)

zk = "localhost:2181"
broker = "localhost:9092"

kafka_params = {
    "bootstrap.servers": broker,
    "auto.offset.reset": "smallest",
    "group.id": "test.group"
}

kafka_stream = KafkaUtils.createDirectStream(ssc,
                                             ['test.avro'],
                                             kafkaParams=kafka_params,
                                             valueDecoder=decoder)

messages = kafka_stream.map(lambda x: x[1])
messages.pprint()

ssc.start()
ssc.awaitTermination()