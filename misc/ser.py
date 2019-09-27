#!python
"""
Kafka Consumer/Producer Java and Python API has problems handling messages with
$'\n' characters [1]. This program consumes a multiline message from stdin and
writes its hex-encoding to stdout. The latter can be pushed to Kafka as a single
message.

[1] https://stackoverflow.com/questions/52151816/push-multiple-line-text-as-one-message-in-a-kafka-topic
"""

import sys, binascii

for l in sys.stdin.buffer:
    sys.stdout.buffer.write(binascii.hexlify(l))

#sys.stdout.buffer.write(b'\n')
