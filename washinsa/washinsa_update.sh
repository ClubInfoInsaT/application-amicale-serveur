#!/bin/bash

source ../venv/bin/activate

touch lock
python3 washinsa_handler.py > log 2> err
rm lock

deactivate
