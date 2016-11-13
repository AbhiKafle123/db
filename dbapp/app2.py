#! /usr/bin/python
from flask import Flask, redirect, url_for, session, request, render_template
from flask_oauth import OAuth
import os
import requests
import json
from pymongo import MongoClient


SECRET_KEY = 'development key'
DEBUG = True
FACEBOOK_APP_ID = '1664088927192847'
FACEBOOK_APP_SECRET = '745acb1c7b53c9e27babd3d9f15a852d'


app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
oauth = OAuth()

# Database connection
client = MongoClient()
db = client.test


places_json = 0
likes_json = 0
friends_json = 0
access_token = 0


facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'user_friends, user_likes, user_location, user_tagged_places, user_photos'}
)


@app.route("/")
def main():
    # jsondata = getJsonData()
    # print (type(jsondata))
    return render_template("login.html",template_folder='templates')


@app.route('/signup')
def index():
    return redirect(url_for('login'))


@app.route('/login')
def login():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))



@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    global access_token
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    access_token = str(resp['access_token'])
    getResponse()
    return 'Logged in as id=%s name=%s redirect=%s session token=%s' % \
        (me.data['id'], me.data['name'], resp['access_token'], request.args.get('next'))


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')


def getAllData(response, page = True):
    data = response['data']
    count = 0
    while ('paging' in response) and page:
        count += 1
	if 'next' in response['paging']:
        	nexturl = response['paging']['next']
        	response = requests.get(nexturl).json()
        	data.extend(response['data'])
    	else:
		break
    return data

def getResponse():
    response = os.system('wget "https://graph.facebook.com/v2.8/me?fields=id,name,likes{category,name,fan_count},friends,tagged_places&access_token=%s" -O all3.json'%(access_token) )
    response = requests.get('https://graph.facebook.com/v2.8/me?fields=id,name,likes{category,name,fan_count},friends,tagged_places&access_token=%s' % (access_token))

    global account_response
    account_response = requests.get('https://graph.facebook.com/v2.8/me/?access_token=%s' % (access_token)).json()
    likes_response = requests.get('https://graph.facebook.com/v2.8/me/likes?fields=category,name&limit=100&access_token=%s' % (access_token)).json()
    friends_response = requests.get('https://graph.facebook.com/v2.8/me/friends?fields=name&limit=100&access_token=%s' % (access_token)).json()
    places_response = requests.get('https://graph.facebook.com/v2.8/me/tagged_places?limit=100&access_token=%s' % (access_token)).json()

    likes = getAllData(likes_response)
    friends = getAllData(friends_response, False)
    places = getAllData(places_response, False)
    user_id = account_response['id']

    global places_json
    places_json = {"_id": user_id, "places": places}
    global friends_json
    friends_json = {"_id": user_id, "friends": friends}
    global likes_json
    likes_json = {"_id": user_id, "likes": likes}
    insertintodb()


def insertintodb():
    try:
        results = db.places.insert(places_json)
        friends = db.friends.insert(friends_json)
        likes = db.likes.insert(likes_json)
        user_account = db.users.insert({"_id" : account_response['id'],"name" : account_response['name']})
    except:
        pass


@app.route('/')
@app.route('/show')
def show():

    me = facebook.get('/me')
    result = db.likes.aggregate([{"$match":{"_id":{"$in":[me.data['id'],"1006051672784344"]}}},{"$group":{"_id":0,"set1":{"$first":"$likes"},"set2":{"$last":"$likes"}}},{"$project":{"commonToBoth":{"$setIntersection":["$set1","$set2"]},"_id":0}}])
    likes = list(result)
    result = db.places.aggregate([{"$match":{"_id":{"$in":[me.data['id'],"1006051672784344"]}}},{"$group":{"_id":0,"set1":{"$first":"$places.place.name"},"set2":{"$last":"$places.place.name"}}},{"$project":{"commonToBoth":{"$setIntersection":["$set1","$set2"]},"_id":0}}])
    places = list(result)
    result = db.friends.aggregate([{"$match":{"_id":{"$in":[me.data['id'],"1006051672784344"]}}},{"$group":{"_id":0,"set1":{"$first":"$friends.name"},"set2":{"$last":"$friends.name"}}},{"$project":{"commonToBoth":{"$setIntersection":["$set1","$set2"]},"_id":0}}])
    friends = list(result)

    likes = likes[0]['commonToBoth']
    categories = set([l['category'] for l in likes])
    result_likes = [{"name":"Likes","children":[{"name":c,"children":[{"name":l["name"]} for l in likes if l['category'] == c]} for c in categories]}]

    places = places[0]['commonToBoth']
    result_places = [{"name":"Places Visited","children":[{"name":p} for p in places]}]

    friends = friends[0]['commonToBoth']
    result_friends = [{"name":"Friends","children":[{"name":f} for f in friends]}]


    all_json ={"name":"Commanalities", "children": result_likes + result_places + result_friends}
    print json.dumps(all_json)
    return "aalu"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
