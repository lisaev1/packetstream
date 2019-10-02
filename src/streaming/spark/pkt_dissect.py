#!python3

# -----------------------------------------------------------------------------
# Modules
# -----------------------------------------------------------------------------
import pkt_dissect_mod as common

import pyspark
import pyspark.streaming as pyspark_streaming
import pyspark.streaming.kafka as pyspark_kafka

import scapy.all as scapy

# -----------------------------------------------------------------------------
# Main program
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    #
    # Setup
    #

    #-- define spark usual and streaming contexts
    cont_0 = pyspark.SparkContext(appName = "pkt_dissector")
    cont_0.setLogLevel("ERROR")
    s_cont_0 = pyspark_streaming.StreamingContext(cont_0, 5)

    #-- kafka integration (notice, that we receive packets as a bytes struct)
    brokers = "192.168.122.71:9092,192.168.122.72:9092,192.168.122.73:9092"
    kafka_dstream = pyspark_kafka.KafkaUtils.createDirectStream(
            s_cont_0, ["test1"],
            {"metadata.broker.list": brokers},
            valueDecoder = lambda x: bytes(x)
    )

    #
    # Lazy evaluation rules
    #
    #-- Kafka message comes as a 2-tuple: (key, value). The code below will
    #-- select the actual message (i.e. packet) and dissects it.
    pkts = kafka_dstream.map(lambda x: scapy.Ether(x[1]))
    filtered_pkts = pkts.filter(common._pkt_filter). \
            map(lambda x: (x, x.summary()))

    #-- DEBUG
    #-- print to the console
    filtered_pkts.pprint()
    
    #
    # Driver code
    #
    #-- start the stream and wait until it is terminated
    s_cont_0.start()
    s_cont_0.awaitTermination()
