from flask import Flask, render_template, json, request

app = Flask(__name__)

# mysql = MySQL()
# My SQL configurations
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
# app.config['MYSQL_DATABASE_DB'] = 'BucketList'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# mysql.init_app(app)

#create mysql connection
# conn = mysql.connect()
# cursor = conn.cursor()

def getJsonData():
    jsondata = json.load(open("data/data.json"))
    return jsondata 

@app.route("/")
def main():
	# jsondata = getJsonData()
	# print (type(jsondata))
	return render_template("login.html",template_folder='templates')

@app.route('/signup')
def showSignUp():
	return render_template('index.html')

@app.route('/ShowsignUp', methods=['POST'])
def signUp():
	# read the posted values from the UI
	_name = request.form['inputName']
	_email = request.form['inputEmail']
	_password = request.form['inputPassword']

	# validate the received values
	if _name and _email and _password:
		_hashed_password = generate_password_hash(_password)
		cursor.callproc('sp_createUSer', (_name, _email, _hashed_password))
		return json.dumps({'html': '<span>All fields good </span>'})
	else:
		return json.dumps({'html': '<span>Enter the required fields'})

if __name__ == "__main__":
	app.run()

# 
