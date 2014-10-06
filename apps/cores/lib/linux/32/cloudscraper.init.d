#! /bin/sh
### BEGIN INIT INFO
# Provides:          cloudscraper
# Required-Start:    $local_fs $network $remote_fs $syslog
# Required-Stop:     $local_fs $network $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Cloudscraper Service
# Description:       Cloudscraper Service 1.0.0
### END INIT INFO

# Author: Bratislav Stojanovic <support@cloudscraper.ca>

# Do NOT "set -e"

# Set variables
CS_ROOT=/var/www/cloudscraper_osse
START_SCRIPT="$CS_ROOT"/apps/cores/bin/linux/32/start.sh
STOP_SCRIPT="$CS_ROOT"/apps/cores/bin/linux/32/stop.sh
PID="$CS_ROOT"/apps/cores/jsvc.pid
USER=brat

do_start()
{
    $START_SCRIPT "$USER" "$CS_ROOT" 
}

do_stop()
{
    $STOP_SCRIPT "$USER" "$CS_ROOT"
}

case "$1" in
    start)
        do_start
            ;;
    stop)
        do_stop
            ;;
    restart)
        if [ -f "$PID" ]; then
            do_stop
            do_start
        else
            echo "Service not running, will do nothing"
            exit 1
        fi
            ;;
    *)
            echo "usage: cloudscraper {start|stop|restart}" >&2
            exit 3
            ;;
esac

:
