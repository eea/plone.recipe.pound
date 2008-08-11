#!/usr/bin/env bash
BUILDOUT_PATH=""
POUND_RUNNER="$poundbin"
POUND_CFG="$poundcfg"
POUND_PID="$poundpid"
SSD_PID="${poundpid}.daemon.pid"
POUND_USER="$user"
USER=\$(whoami)


stop() {
    echo "Stopping pound"
    sleep 2
    # little hack if we come from start-stop-daemon
    for PIDFILE in \$POUND_PID \$SSD_PID;do
        if [[ -f "\$PIDFILE" ]];then
            kill `cat "\$PIDFILE"` 2>/dev/null
            if [ -f "\$PIDFILE" ]
            then
                rm "\$PIDFILE"
            fi
        fi
    done
}

start() {
    echo "Starting pound"
    LAUNCH_ARGS="-f \$POUND_CFG -p \$POUND_PID"
    if [[ \$USER != root ]];then
        "\$POUND_RUNNER" \$LAUNCH_ARGS
    else
        # start-stop-daemon give us mean to start a process with an user
        # without configured shell.
        # We search it in the firstime
        ssd=\$(which start-stop-daemon 2>/dev/null)
        if [[ ! -f "\$ssd" ]]; then
            ssd=/sbin/start-stop/daemon
        fi
        # fall back on su or set ssd arguments
        if [[ ! -f "\$ssd" ]]; then
            su "\$POUND_USER" -c "\$POUND_RUNNER \$LAUNCH_ARGS"
        else
            ssd="\$ssd --start --user \$POUND_USER --quiet --background"
            ssd="\$ssd  -p \$SSD_PID -m  --exec \$POUND_RUNNER -- \$LAUNCH_ARGS"
            \$ssd
        fi
    fi
    sleep 2
}

case \$1 in

    start)
    start
    ;;

    stop)
    stop
    ;;

    restart)
    echo "Restarting pound"
    stop
    sleep 4
    start
    ;;

    status)
    if [ -f \$POUND_PID ]
    then
        PID=`cat "\$POUND_PID"`
        echo "Pound running - process \$PID"
    else
        echo "Pound not running"
    fi
    ;;

    *)
    echo "Usage: pound (start|stop|restart|status)"
    ;;

esac

\# vim:set ft=sh:
