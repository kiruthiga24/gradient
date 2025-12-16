#!/bin/bash

LOG_FILE=/home/cron.log

echo "Cron started at $(date)" >> $LOG_FILE

curl -X POST http://127.0.0.1:5000/signals/run >> $LOG_FILE 2>1&
curl -X POST http://127.0.0.1:5000/run/churn-risk >> $LOG_FILE 2>1&
curl -X POST http://127.0.0.1:5000/run/expansion/from-table >> $LOG_FILE 2>1&
curl -X POST http://127.0.0.1:5000/run/quality/from-table >> $LOG_FILE 2>1&
curl -X POST http://127.0.0.1:5000/run/supply-risk >> $LOG_FILE 2>1&
curl -X POST http://127.0.0.1:5000/run/qbr/from-table >> $LOG_FILE 2>1&


echo "Cron finished at $(date)" >> $LOG_FILE
