# PacketStream security considerations (encrypting data ingestion)

## Table of Contents
1. Overview
2. Setup instructions

## Overview

At the ingestion stage, we need to transmit highly sensitive data over the internet. There are several ways to accomplish this: (1) use Kafka-producer over TLS (2) use ssh tunnels.

The 1st solution is what most people would do, but it is not optimal because it requires a PKI infrastructure (getting a cert with a CA and hoping that the data producer has it in its store). Therefore, we choose the 2nd approach when communications between producer (client) and Kafka cluster are wrapped in an ssh tunnel, similar to X11 forwarding.

## Setup instructions

First, we create an unprivileged user on each Kafka node, called "kafka-producer", with an ~/.ssh directory:
```
[root@broker23 ~]# useradd -m -s /usr/bin/nologin kafka-producer
[root@broker23 ~]# passwd -l kafka-producer
[root@broker23 ~]# install -dm 700 /home/kafka-producer/.ssh
```

Next, we generate a passwordless ssh keypair *for the entire Kafka cluster*:
```
[user@workstation ~]$ ssh-keygen -t rsa -N "" -f /tmp/kafka-key
```
and embed the public part into each broker:
```
[root@broker23 ~]# cat /home/kafka-producer/.ssh/authorized_keys
ssh-rsa AAAAB3Nz...
```
The private part of the key is given to a 
