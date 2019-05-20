#!/usr/bin/env bash

$SPARK_HOME/bin/spark-submit --packages org.apache.spark:spark-avro_2.11:2.4.0,org.apache.spark:spark-sql-kafka-0-10_2.11:2.1.0,org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.2 ./avro/avro_stream.py