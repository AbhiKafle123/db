#!/usr/bin/python
#Pulling data from graph api in a single JSON file
# Name,ID followed by Likes followed by tagged_places followed by friends


import os
import requests
import json
access_token = raw_input()


# response = os.system('wget "https://graph.facebook.com/v2.8/me?fields=id,name,likes{category,name,fan_count},friends,tagged_places&access_token=%s" -O all3.json'%(access_token) )
#response = requests.get('https://graph.facebook.com/v2.8/me?fields=id,name,likes{category,name,fan_count},friends,tagged_places&access_token=%s' % (access_token))
response = requests.get('https://graph.facebook.com/v2.8/me/likes?fields=category,name&limit=100&access_token=%s' % (access_token)).json()

# print response['paging']['next']
likes = response['data']
count = 0
while 'paging' in response:
#	print count
#	count += 1
	nexturl = response['paging']['next']
	response = requests.get(nexturl).json()
	likes.extend(response['data'])
print likes
#print sum([1 for l in likes])




