#/bin/bash

cd /opt/deal-bot

source environment.sh
export PATH=$PATH:/opt/chrome
python data_import.py