#!/bin/sh
JSVC_USER="$1"
JAVA_HOME=/usr/lib/jvm/java-7-openjdk-i386
DAEMON_HOME="$2"/apps/cores
PID_FILE="$DAEMON_HOME/jsvc.pid"
XMS=256M
XMX=512M
CLASSPATH=\
.:\
$CLASSPATH:\
$DAEMON_HOME/tika-server-1.5-SNAPSHOT-PATCHED.jar
echo "Stopping Cloudscraper Service..."
$DAEMON_HOME/bin/linux/32/jsvc32_ubuntu \
-jvm server \
-home $JAVA_HOME \
-user $JSVC_USER \
-stop \
-pidfile $PID_FILE \
-outfile $DAEMON_HOME/logs/jsvc.out \
-errfile '&1' \
-cp $CLASSPATH \
-debug \
-cwd $DAEMON_HOME \
-DLOG_FILE=$DAEMON_HOME/logs/cloudscraper.log \
-Djava.awt.headless=true \
-Xms$XMS \
-Xmx$XMX \
org.apache.tika.server.TikaServerDaemon stop
