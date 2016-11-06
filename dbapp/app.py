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


access_token = 0


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
    # print resp
    access_token = str(resp['access_token'])
    print "\nInside"
    print access_token
    print "\n"

    print "\n"
    print type(access_token)
    print "\n"
    getResponse()
    return 'Logged in as id=%s name=%s redirect=%s session token=%s' % \
        (me.data['id'], me.data['name'], resp['access_token'], request.args.get('next'))



# access_token = "EAAXpeuVhRw8BAEAfliZAaIsi9dyU5nQFjAQkAFE4PJGkph8edAJ0D9oWAKSuwRL3vo5b6kZBHVnnr0aJ9iXRPSBv9XtwEeoZCVVCcf1aGX6ohyp1VMrLlReb9JnmhHuapZCUcZAqoAKeXSXtMWhNygKLsrGcORUrNqBO1m304PAZDZD"
@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')


client = MongoClient()
db = client.test

places_json = 0
likes_json = 0
friends_json =0


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

def getResponse():
    print "\nOutsideside"
    print access_token
    print "\n"
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

    # print {"id":1, "likes":likes}
    user_id = account_response['id']
    # print len(friends)
    # print len(places)

    #print user_id
    global places_json 
    places_json = {"id":user_id, "places":places}
    global friends_json 
    friends_json = {"id":user_id, "friends":friends}
    global likes_json
    likes_json = {"id":user_id, "likes":likes}
    insertintodb()
# print places[len(places)-1]
#print account_response
#print places_json

def insertintodb():
    results = db.places.insert(places_json)
    friends = db.friends.insert(friends_json)
    likes = db.likes.insert(likes_json)
    user_account = db.users.insert(account_response)
    


if __name__ == '__main__':
    app.run(host='0.0.0.0')