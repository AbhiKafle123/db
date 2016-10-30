#!/usr/bin/python
#Pulling data from graph api in a single JSON file
# Name,ID followed by Likes followed by tagged_places followed by friends


import os
import requests
import json
from pymongo import MongoClient

client = MongoClient()
db = client.test


access_token = raw_input()

def getAllData(response, page = True):
	data = response['data']
	count = 0
	while ('paging' in response) and page:
		print count
		count += 1
		nexturl = response['paging']['next']
		response = requests.get(nexturl).json()
		data.extend(response['data'])
	print len(data)
	return data


# response = os.system('wget "https://graph.facebook.com/v2.8/me?fields=id,name,likes{category,name,fan_count},friends,tagged_places&access_token=%s" -O all3.json'%(access_token) )
#response = requests.get('https://graph.facebook.com/v2.8/me?fields=id,name,likes{category,name,fan_count},friends,tagged_places&access_token=%s' % (access_token))
account_response = requests.get('https://graph.facebook.com/v2.8/me/?access_token=%s' % (access_token)).json()
likes_response = requests.get('https://graph.facebook.com/v2.8/me/likes?fields=category,name&limit=100&access_token=%s' % (access_token)).json()
friends_response = requests.get('https://graph.facebook.com/v2.8/me/friends?fields=name&limit=100&access_token=%s' % (access_token)).json()
places_response = requests.get('https://graph.facebook.com/v2.8/me/tagged_places?limit=100&access_token=%s' % (access_token)).json()

likes = getAllData(likes_response)
friends = getAllData(friends_response, False)
places = getAllData(places_response, False)

# print {"id":1, "likes":likes}
user_id = account_response['id']
# print len(friends)
# print len(places)

print user_id
places_json = {"id":user_id, "places":places}
friends_json = {"id":user_id, "friends":friends}
likes_json = {"id":user_id, "likes":likes}
# print places[len(places)-1]
print account_response

# results = db.places.insert(places_json)
# friends = db.friends.insert(friends_json)
# likes = db.likes.insert(likes_json)
# user_account = db.users.insert(account_response)