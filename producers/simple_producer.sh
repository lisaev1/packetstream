#!bash

declare brokers topic port

#-- default port for Kafka listeners
port=9092

#-- target topic
topic="$1"
shift

#-- build list of brokers
brokers=""
for b in "$@"; do
	brokers="${brokers},${b}:${port}"
done
brokers="${brokers:1}"

kafka-console-producer.sh --broker-list "$brokers" --topic "$topic"
