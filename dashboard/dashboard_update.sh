#!/bin/bash

# Update washing machines
cd "$HOME"/public_html/washinsa && ./washinsa_update.sh

# Update the dashboard with the new machine list
touch lock
python3 handler.py > log 2> err
rm lock