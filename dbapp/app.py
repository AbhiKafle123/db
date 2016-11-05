#! /usr/bin/python
from flask import Flask, redirect, url_for, session, request, render_template
from flask_oauth import OAuth


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


@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    return 'Logged in as id=%s name=%s redirect=%s session token=%s' % \
        (me.data['id'], me.data['name'], resp['access_token'], request.args.get('next'))


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')
    print session.get('oauth_token')


if __name__ == '__main__':
    app.run()
