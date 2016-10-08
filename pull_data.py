import os

access_token = raw_input()

print os.system('curl -sS \'https://graph.facebook.com/v2.8/me/likes?limit=1000&access_token={}\' >> likes.json'.format(access_token) )
print os.system('curl -sS \'https://graph.facebook.com/v2.8/me/tagged_places?limit=500&access_token={}\' >> places.json'.format(access_token) )

