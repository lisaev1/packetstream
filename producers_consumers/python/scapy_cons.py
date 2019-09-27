#!python
"""
Kafka consumer that parses scapy packets in messages and prints them
"""

import kafka, common, sys
import scapy.all as scapy

#-- parse cmdline options
pcap_f, topic, srv_list = common._parseopts()

#-- sanity checks
if (len(srv_list) == 0):
    print("Please specify at least one Kafka broker! Aborting.")
    sys.exit(1)

#--set up the consumer object
consumer = kafka.KafkaConsumer(topic, bootstrap_servers = srv_list)

#-- iterate over messages
for m in consumer:
    p = scapy.Ether(m.value)
    print(p.summary)

consumer.close()
