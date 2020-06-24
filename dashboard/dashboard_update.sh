#!/bin/bash

# Update washing machines
cd "$HOME"/public_html/v2/washinsa && ./washinsa_update.sh

cd "$HOME"/public_html/v2/dashboard || exit

# Update the dashboard with the new machine list
touch lock
python3 dashboard_handler.py > log 2> err
rm lock