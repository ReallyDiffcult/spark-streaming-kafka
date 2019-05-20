#!/usr/bin/env python

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import json
import os


import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.2 pyspark-shell'

def decoder(msg_value):
    event_dict = msg_value.decode("utf-8")
    return event_dict
    

# Create a spark context
sc = SparkContext(appName="SparkStreamingTest")
ssc = StreamingContext(sc, 10)

zk = "localhost:2181"
broker = "localhost:9092"

kafka_params = {
    "bootstrap.servers": broker,
    "auto.offset.reset": "smallest",
    "group.id": "test.group"
}

kafka_stream = KafkaUtils.createDirectStream(ssc,
                                             topics=['test.json'],
                                             kafkaParams=kafka_params,
                                             valueDecoder=decoder
)

messages = kafka_stream.map(lambda x: x[1])
messages.pprint()

ssc.start()
ssc.awaitTermination()