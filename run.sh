#!/bin/bash

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOGFILEPATH="./log/aexol_log_$TIMESTAMP.log"

if [ ! -d log ];
then
    mkdir ./log/
    echo "No /log/ directory for log file storage found. Created it automatically."
fi

echo "Log file name for this execution : $LOGFILEPATH"

nohup python3 ./bot.py 1>"$LOGFILEPATH" 2>&1 &
echo "program executed"