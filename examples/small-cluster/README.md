# Example configs for development clusters

This directory contains configs for small clusters that were used during the development. The underlying operating system for all VMs is Arch Linux (please see the archlinux/ directory at the repo root for package sources).

## Table of Contents
1. Kafka & Zookeeper
2. Spark
3. Cassandra

## Kafka & Zookeeper

The Kafka/Zookeeper cluster has 3 brokers (minimum number which allows a Zookeeper consensus) and was installed using zookeeper and kafka packages. We didn't use the Zookeeper scripts bundles with Kafka.

## Spark

Our Spark cluster also has 3 nodes and is driven by a pyspark program. It consumes packet streams from the Kafka cluster, decodes and processes them, and writes filtered results to the Cassandra database.

## Cassandra
