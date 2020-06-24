#!/bin/bash

# A token is required to access the facebook public page
# This token must be saved in a file named "token" in the same folder as this script
# /!\ Do not sync this token with git /!\

touch lock
token=$(cat token)
curl "https://graph.facebook.com/v7.0/amicale.deseleves/published_posts?fields=full_picture,message,permalink_url,created_time&date_format=U&access_token=$token" > facebook_data.json
rm lock
