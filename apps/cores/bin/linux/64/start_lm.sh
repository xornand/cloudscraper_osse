#!/bin/sh
JSVC_USER="$1"
JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64
DAEMON_HOME="$2"/apps/cores
PID_FILE="$DAEMON_HOME/jsvc_lm.pid"
XMS=64M
XMX=128M
CLASSPATH=\
.:\
$CLASSPATH:\
$DAEMON_HOME/license-server-1.0.jar
echo "Starting Cloudscraper License Service..."
$DAEMON_HOME/jsvc64_ubuntu \
-jvm server \
-home $JAVA_HOME \
-user $JSVC_USER \
-wait 10 \
-pidfile $PID_FILE \
-outfile $DAEMON_HOME/logs/jsvc_lm.out \
-errfile '&1' \
-cp $CLASSPATH \
-debug \
-cwd $DAEMON_HOME \
-DLOG_FILE=$DAEMON_HOME/logs/cloudscraper_lm.log \
-Djava.awt.headless=true \
-Xms$XMS \
-Xmx$XMX \
ca.cloudscraper.lm.LicenseServerDaemon start
