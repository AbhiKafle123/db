#!/usr/bin/python
#Pulling data from graph api in a single JSON file
# Name,ID followed by Likes followed by tagged_places followed by friends


import os

access_token = raw_input()
print os.system('curl -sS \'https://graph.facebook.com/v2.8/me?limit=1000&access_token={}\' >> places.json'.format(access_token) )

print os.system('curl -sS \'https://graph.facebook.com/v2.8/me/likes?limit=1000&fields=category,name&access_token={}\' >> places.json'.format(access_token) )

print os.system('curl -sS \'https://graph.facebook.com/v2.8/me/tagged_places?limit=500&access_token={}\' >> places.json'.format(access_token) )

print os.system('curl -sS \'https://graph.facebook.com/v2.8/me/friends?limit=1000&access_token={}\' >> places.json'.format(access_token) )
