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

* * * * * cd $HOME/public_html/facebook/ && ./facebook_update.sh >/dev/null 2>&1
# Call 2 times, one with a 30 sec delay
* * * * * cd $HOME/public_html/ && ./update_washinsa.sh >/dev/null 2>&1
* * * * * cd $HOME/public_html/ && (sleep 30 ; ./update_washinsa.sh) >/dev/null 2>&1

0 0 * * * cd $HOME/public_html/menu/ && ./menu_update.sh >/dev/null 2>&1

# Add at the end of the command to stop emails
# >/dev/null 2>&1


