#!/bin/sh
JSVC_USER="$1"
JAVA_HOME=/usr/lib/jvm/jre-1.7.0-openjdk.x86_64
DAEMON_HOME="$2"/apps/cores
PID_FILE="$DAEMON_HOME/jsvc_lm.pid"
XMS=64M
XMX=128M
CLASSPATH=\
.:\
$CLASSPATH:\
$DAEMON_HOME/license-server-1.0.jar
echo "Stopping Cloudscraper License Service..."
$DAEMON_HOME/bin/linux/64/jsvc64_ubuntu \
-jvm server \
-home $JAVA_HOME \
-user $JSVC_USER \
-stop \
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
ca.cloudscraper.lm.LicenseServerDaemon stop
