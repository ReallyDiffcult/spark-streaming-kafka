# Spark Streaming with Kafka

Sample code showing how to use Spark Streaming with Kafka.

## Dependencies

* [Apache Spark](https://spark.apache.org/downloads.html) (tested with 2.3.3 pre-built for Hadoop)
* [Python](https://www.anaconda.com/distribution/#download-section) (tested with 3.7.3)
* [Apache Avro](http://apache.osuosl.org/avro/avro-1.8.2/py3/) for Python 3 (tested with 1.8.2)
* [Docker](https://docs.docker.com/install/)

## Notes on Running Apache Spark

If you're using Apache Spark with pre-built Hadoop, it's highly recommended to create a `SPARK_HOME` environment variable in your `~/.bash_profile` or `~/.zshrc` file like so:
```
# Spark
export SPARK_HOME="/Users/robert.dempsey/Applications/spark-2.3.3-bin-hadoop2.7"
export PATH=$PATH:$SPARK_HOME/bin
```

This makes it easy to call the Spark executables, and the shell scripts in this repo rely on that variable existing.

## Installation

Clone this repo and cd into the directory.

Create a new Python 3.7.3 environment, activate it, and install the additional packages:
```
$ conda create -n pyspark_env python=3.7.3
$ source activate pyspark_env
$ pip install -r requirements.txt
```

Download and install Apache Avro:
```
$ tar xvf avro-1.8.2.tar.gz
$ cd avro-1.8.2
$ sudo python setup.py install
$ python
>>> import avro # should not raise ImportError
```

## Run

There are examples showing parsing JSON and avro. They run the same way, so let's see how to run the avro example. From the root directory:

Launch the Docker containers:
```
$ docker-compose up -d
$ docker ps
```

In one terminal window, run the avro producer:
```
$ python avro/avro_producer.py
```

In another terminal window, run the avro consumer as a check:
```
$ python avro/avro_consumer.py
```

If everything is working you should see the messages being produced to Kafka by the producer script and consumed by the consumer script.

Now, stop the consumer script and run the shell script to use Spark Streaming:
```
$ chmod +x spark_submit_avro.sh
$ ./spark_submit_avro.sh
```

It takes a minute for Spark to get going, however once it does you should see output like this:
```
-------------------------------------------
Time: 2019-05-20 05:20:15
-------------------------------------------
{'name': 'Robert', 'favorite_number': 0, 'favorite_color': 'blue'}
{'name': 'Robert', 'favorite_number': 1, 'favorite_color': 'blue'}
{'name': 'Robert', 'favorite_number': 2, 'favorite_color': 'blue'}
{'name': 'Robert', 'favorite_number': 3, 'favorite_color': 'blue'}
{'name': 'Robert', 'favorite_number': 4, 'favorite_color': 'blue'}
{'name': 'Robert', 'favorite_number': 5, 'favorite_color': 'blue'}
{'name': 'Robert', 'favorite_number': 6, 'favorite_color': 'blue'}
{'name': 'Robert', 'favorite_number': 7, 'favorite_color': 'blue'}
{'name': 'Robert', 'favorite_number': 8, 'favorite_color': 'blue'}
{'name': 'Robert', 'favorite_number': 9, 'favorite_color': 'blue'}
```

As Spark is processing the Kafka stream in mini-batches, you'll continue to see messages like this while the producer continues to produce events.