#!/usr/bin/env bash

export JAVA_HOME=/usr/lib/jvm/default-runtime

if (command -v hadoop 2> /dev/null); then
    export SPARK_DIST_CLASSPATH="$(hadoop classpath)"
else
    export SPARK_DIST_CLASSPATH=""
fi

export SPARK_MASTER_HOST=spark-node1 \
        SPARK_LOCAL_IP=192.168.122.82
