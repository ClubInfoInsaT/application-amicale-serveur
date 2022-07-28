#!/bin/bash

source ../venv/bin/activate

touch lock
python3 planex_handler.py > log 2> err
rm lock

deactivate
