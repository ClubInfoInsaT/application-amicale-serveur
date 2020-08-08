#!/bin/bash

source venv/bin/activate

touch lock
curl "https://webservices-v2.crous-mobile.fr/ws/v1/regions/5/restaurants/114/menus" > menu_data.json && python3 menu_handler.py > log 2> err
rm lock

deactivate
