from flask import Flask
import json
from pymongo import MongoClient
client = MongoClient()
app = Flask(__name__)
db = client.test



print "ok"
@app.route('/')
@app.route('/show')
def show():
	#print "test"
	#print dir(db)
	#	result = []
	#	result = db.places.aggregate([ { "$match": { "_id": { "$in": ["10211143854462012", "1006051672784344"] } } }, { "$group": { "_id": 0, "set1": { "$first": "$places.place" }, "set2": { "$last": "$places.place" } } }, { "$project": { "commonToBoth": { "$setIntersection": [ "$set1", "$set2" ] }, "_id": 0 } } ]) 
	result = db.likes.aggregate([ { "$match": { "_id": { "$in": ["10211143854462012", "1006051672784344"] } } }, { "$group": { "_id": 0, "set1": { "$first": "$likes" }, "set2": { "$last": "$likes" } } }, { "$project": { "commonToBoth": { "$setIntersection": [ "$set1", "$set2" ] }, "_id": 0 } } ]) 
	likes = list(result)
	#print result
	result = db.places.aggregate([{"$match":{"_id":{"$in":["10211143854462012","1006051672784344"]}}},{"$group":{"_id":0,"set1":{"$first":"$places.place.name"},"set2":{"$last":"$places.place.name"}}},{"$project":{"commonToBoth":{"$setIntersection":["$set1","$set2"]},"_id":0}}])
	places = list(result)
	#print result
	result = db.friends.aggregate([{"$match":{"_id":{"$in":["10211143854462012","1006051672784344"]}}},{"$group":{"_id":0,"set1":{"$first":"$friends.name"},"set2":{"$last":"$friends.name"}}},{"$project":{"commonToBoth":{"$setIntersection":["$set1","$set2"]},"_id":0}}])
	friends = list(result)
	#print result
	likes = likes[0]['commonToBoth']
	categories = set([l['category'] for l in likes])
	result_likes = [{"name":c,"children":[{"name":l['name']} for l in likes if l['category'] == c]} for c in categories]

	places = places[0]['commonToBoth']
	result_places = {"name":"Places Visited","children":[{"name":p} for p in places]}

	friends = friends[0]['commonToBoth']
	result_friends = {"name":"Friends","children":[{"name":f} for f in friends]}


	return "aalu"


	#return user.find()

if __name__== "__main__":
	app.run(host='0.0.0.0', port=5000, debug=True)
