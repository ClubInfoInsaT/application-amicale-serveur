#/bin/bash!

cd $HOME/public_html/washinsa
# update washing machine list
php index.php

cd ../expo_notifications
# watch for new notifications with the new list
python3 handler.py

cd ../dashboard
# Update the dashboard
python3 handler.py > log 2> err 
