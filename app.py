from flask import Flask
import models

DEBUG = True
PORT = 8000

#initialize instance of flask clasas
app = Flask(__name__)

@app.before_request
def before_request():
	#connect to DB before every request
	g.db = models.DATABASE
	g.db.connect()

@app.after_request
def after_request():
	#close connection to DB after every request
	g.db.close()
	return response

#default route
@app.route('/')
def hello():
	return 'Hello'


if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)