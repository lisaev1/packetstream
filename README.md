# PacketStream

## Table of Contents
1. Description
1. Directory layout
1. Basic operation
2. License

## Description

This repository contains my Insight Data Engineering project (NY 2019), whose goal is to develop a platform for the analysis of packet captures streamed from customer's servers.

## Layout

There are three top-level directories: `src/` for code sources, `deployment/` -- package sources and example configuration, and `input/`(`output/`) that holds a sample input packet capture file (table in the Cassandra database after the pipeline). Specifically:
```
/
|
|- app/				# frontend code
|- slides/			# presentation slides
|- src/
|  |- streaming/		# codes that deal with processing of streaming data
|  |- misc/			# miscellaneous utilities
|  `- producers_consumers/	# Kafka producers and consumers
|
|- deployment/
|  |- archlinux/		# Arch Linux packages for the pipeline
|  |- examples/			# Configuration snippets for development clusters
|  `- security/			# (WIP) security considerations
|
|- input/
`- output/
```

## Basic operation

The network packets are sent from customers' machines into Kafka cluster, then are pulled by Spark Streaming engine for parsing, and finally pushed into the Cassandra database for storage and query. Please see `slides/slides.pdf` for a more detailed presentation.

## License

No license or copyright.
