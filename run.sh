#!/bin/bash

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOGFILEPATH="./log/aexol_log_$TIMESTAMP.log"

if [ ! -d log ];
then
    mkdir ./log/
fi

nohup python3 ./bot.py 1>"$LOGFILEPATH" 2>&1 &