#!/bin/sh

NAME="LibreSpeed Speedtest"
PKG_DIR="/usr/local/AppCentral/LibreSpeedtest"
PIDFILE="${PKG_DIR}/var/lighttpd.pid"
CONF="${PKG_DIR}/var/lighttpd.conf"

case "$1" in
    start)
        if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
            echo "$NAME is already running"
            exit 0
        fi
        echo "Starting $NAME"
        lighttpd -f "${CONF}"
    ;;
    stop)
        echo "Stopping $NAME"
        if [ -f "$PIDFILE" ]; then
            kill "$(cat "$PIDFILE")" 2>/dev/null
            rm -f "$PIDFILE"
        fi
        # Safety net if pidfile is missing or stale
        pkill -f "lighttpd -f ${CONF}" 2>/dev/null
    ;;
    restart|force-reload)
        $0 stop
        sleep 2
        $0 start
    ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 2
    ;;
esac
exit 0
