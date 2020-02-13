#!/bin/bash
#
CDIR=`dirname ${0}`
cd ${CDIR}/

nohup python twelite_monitor_logging.py < /dev/null > /dev/null 2>&1  &
echo "Process ID="$!
echo "Remote window security system started."
echo "Remote soil moisture monitoring system started."