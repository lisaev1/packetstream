from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

#-- initialize Spark Context with a proper log level
spark_context = SparkContext(appName = "app1")
spark_context.setLogLevel("INFO")

#-- init Streaming Context with a 5s batch duration
s_stream = StreamingContext(spark_context, 5)

#-- subscribe to a Kafka topic
k_stream = KafkaUtils.createDirectStream(s_stream, ["test1"],
        {"metadata.broker.list": "192.168.122.71:9092"})


