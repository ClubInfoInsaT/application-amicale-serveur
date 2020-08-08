#!/bin/bash

source ../venv/bin/activate

touch lock
python3 facebook_handler.py > log 2> err
rm lock

deactivate
