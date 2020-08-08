#!/bin/bash

touch lock
python3 facebook_handler.py > log 2> err
rm lock
