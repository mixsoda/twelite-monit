#!/bin/bash
#
CDIR=`dirname ${0}`
SHNAME=`basename ${0}`
cd ${CDIR}/

PY_SCRIPT_NAME='twelite_monitor_logging.py'
LAST_PID=`cat pid.txt`

RUNNING_FLAG=`ps -x | awk "/${LAST_PID}/{print \\$0}" | awk "/${PY_SCRIPT_NAME}/{print \\$0}" | wc -l`

if [ ${RUNNING_FLAG} -eq 0 ]; then
    nohup python twelite_monitor_logging.py < /dev/null > /dev/null 2>&1  &
    echo "Remote window security system started."
    echo "Remote soil moisture monitoring system started."
    echo "Process ID="$!
    echo $! > pid.txt
    echo 'TWELITE monit started @ ' `date` >> log.txt
fi
