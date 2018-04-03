#/bin/bash

SCRIPT_NAME=$1

cd /opt/deal-bot

source environment.sh
export PATH=$PATH:/opt/chrome
python $SCRIPT_NAME