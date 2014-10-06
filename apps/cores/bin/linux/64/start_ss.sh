#!/bin/sh
JSVC_USER="$1"
JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64
DAEMON_HOME="$2"/apps/cores
PID_FILE="$DAEMON_HOME/jsvc_ss.pid"
XMS=128M
XMX=512M
CLASSPATH=\
.:\
$CLASSPATH:\
$DAEMON_HOME/suggest-server-1.0.jar
echo "Starting Cloudscraper Suggest Service..."
$DAEMON_HOME/bin/linux/64/jsvc64_ubuntu \
-jvm server \
-home $JAVA_HOME \
-user $JSVC_USER \
-wait 10 \
-pidfile $PID_FILE \
-outfile $DAEMON_HOME/logs/jsvc_ss.out \
-errfile '&1' \
-cp $CLASSPATH \
-debug \
-cwd $DAEMON_HOME \
-DLOG_FILE=$DAEMON_HOME/logs/cloudscraper_ss.log \
-Djava.awt.headless=true \
-Xms$XMS \
-Xmx$XMX \
ca.cloudscraper.SuggestServerDaemon start unix "$3" "$4" "$5"

