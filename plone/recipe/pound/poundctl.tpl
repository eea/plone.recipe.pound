#!/usr/bin/env bash
BUILDOUT_PATH=""
POUND_RUNNER="$poundbin"
POUND_CFG="$poundcfg"
POUND_PID="$poundpid"
LOG_FILENAME="$logfilename"

case \$1 in

start)
echo "Starting pound"
\$POUND_RUNNER -f \$POUND_CFG -p \$POUND_PID &>> \$LOG_FILENAME
sleep 2
;;

stop)
echo "Stopping pound"
sleep 2
kill `cat \$POUND_PID`
if [ -f \$POUND_PID ]
then
rm \$POUND_PID
fi
;;

restart)
echo "Restarting pound"
kill `cat \$POUND_PID`
sleep 4
\$POUND_RUNNER -f \$POUND_CFG -p \$POUND_PID &>> \$LOG_FILENAME
;;

status)
if [ -f \$POUND_PID ]
then
PID=`cat \$POUND_PID`
echo "Pound running - process \$PID"
else
echo "Pound not running"
fi
;;


*)
echo "Usage: pound (start|stop|restart|status)"
;;

esac
