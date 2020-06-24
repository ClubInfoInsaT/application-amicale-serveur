#!/bin/bash

# *     *     *     *     *  command to be executed
# -     -     -     -     -
# |     |     |     |     |
# |     |     |     |     +----- day of week (0 - 6) (Sunday=0)
# |     |     |     +------- month (1 - 12)
# |     |     +--------- day of month (1 - 31)
# |     +----------- hour (0 - 23)
# +------------- min (0 - 59)

# * * * * *  #Runs every minute
# 30 * * * *  #Runs at 30 minutes past the hour
# 45 6 * * *  #Runs at 6:45 am every day
# 45 18 * * *  #Runs at 6:45 pm every day
# 00 1 * * 0  #Runs at 1:00 am every Sunday
# 00 1 * * 7  #Runs at 1:00 am every Sunday
# 00 1 * * Sun  #Runs at 1:00 am every Sunday
# 30 8 1 * *  #Runs at 8:30 am on the first day of every month
# 00 0-23/2 02 07 *  #Runs every other hour on the 2nd of July

# @reboot  #Runs at boot
# @yearly  #Runs once a year [0 0 1 1 *]
# @annually  #Runs once a year [0 0 1 1 *]
# @monthly  #Runs once a month [0 0 1 * *]
# @weekly  #Runs once a week [0 0 * * 0]
# @daily  #Runs once a day [0 0 * * *]
# @midnight  #Runs once a day [0 0 * * *]
# @hourly  #Runs once an hour [0 * * * *]

# Update the menu every day
0 0 * * * cd "$HOME"/public_html/v2/menu/ && ./menu_update.sh >/dev/null 2>&1

# Update facebook data every minute
* * * * * cd "$HOME"/public_html/v2/facebook/ && ./facebook_update.sh >/dev/null 2>&1

# Update the dashboard every 20 sec. The dashboard also update the machine list
# Call 3 times, one with a 20 sec delay, and one with 40 sec, because cron cannot call more than each minute
* * * * * cd "$HOME"/public_html/v2/dashboard && ./dashboard_update.sh >/dev/null 2>&1
* * * * * cd "$HOME"/public_html/v2/dashboard && (sleep 20 ; ./dashboard_update.sh) >/dev/null 2>&1
* * * * * cd "$HOME"/public_html/v2/dashboard && (sleep 40 ; ./dashboard_update.sh) >/dev/null 2>&1

# To stop emails, add the following at the end of each command:
# >/dev/null 2>&1


