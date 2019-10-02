#!python3
"""
Common functions for Kafka packet producer and consumer
"""

import sys, argparse

def _parseopts():
    """
    Parse cmdline options to determine topic, Kafka brokers and input files. The
    file names are provided via optional arguments. Note, that repeated optional
    arguments are not allowed. E.g. -p xxx.csv -p yyy.csv will trigger an error.
    Returns:
        3-tuple (topic, broker list, pcap file)
    """
    ap = argparse.ArgumentParser()

    ap.add_argument("-p", "--pcap", type = str,
            default = ["/dev/null"],
            help = "Packet capture (pcap0 file to parse (default: none)",
            action = "append",
            metavar = "FILE")

    ap.add_argument("-t", "--topic", type = str,
            default = ["sharks"],
            help = "Kafka topic (default: sharks)",
            action = "append",
            metavar = "TOPIC")

    ap.add_argument("-s", "--servers", type = str,
            default = ["192.168.122.71:9092"],
            help = "Kafka broker (default: none). Can be specified multiple times.",
            action = "append",
            metavar = "SERVER:PORT")

    args = ap.parse_args()

    #-- abort if "-p" or "-t" flags are passed more than once
    if (len(args.pcap) > 2):
        s = "pcap files"
    elif (len(args.topic) > 2):
        s = "topics"
    else:
        s = "x"

    if (s != "x"):
        print(f"ERROR: Several {s} passed! Please provide only one.")
        sys.exit(1)

    return (args.pcap[-1], args.topic[-1], args.servers[1:])
