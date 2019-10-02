# PacketStream

## Table of Contents
1. Description
1. Directory layout
2. License

## Description

This repository contains my Insight Data Engineering project (NY 2019), whose goal is to develop a platform for the analysis of packet captures streamed from customer's servers.

## Layout

There are three top-level directories: `src/` for code sources, `deployment/` -- package sources and example configuration, and `input/`(`output/`) that holds a sample input packet capture file (table in the Cassandra database after the pipeline). Specifically:
```
/
|
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

## License

No license or copyright.
