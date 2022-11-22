#!/bin/bash

source ../venv/bin/activate

touch lock
touch planex.json
python3 planex_handler.py > log 2> err
rm lock

deactivate
