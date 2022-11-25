#!/bin/bash

cd "$HOME"/public_html/v2/notification || exit

# Fetch latest notifications from Hawkeye
# Note that is a temporary test solution.
# Notifications should be served from the amicale server
touch lock
wget https://amicale-app-dev.insat.fr/notification/list.json
rm lock

