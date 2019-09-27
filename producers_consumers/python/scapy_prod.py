#!python
"""
Kafka producer for packets stored in a pcap file.
Sends 1 scapy packet per message.
"""

import os, sys, kafka, common
import scapy.all as scapy

#-- parse cmdline options
pcap_f, topic, srv_list = common._parseopts()

#-- sanity checks
if (not os.path.isfile(pcap_f)):
    print(f"File \"{pcap_f}\" does not exist! Aborting.")
    sys.exit(1)

if (len(srv_list) == 0):
    print("Please specify at least one Kafka broker! Aborting.")
    sys.exit(1)

#-- define a producer
producer = kafka.KafkaProducer(bootstrap_servers = srv_list)

#-- read the pcap file
capture = scapy.rdpcap(pcap_f)
for p in capture:
    producer.send(topic, bytes(p))

producer.close()
