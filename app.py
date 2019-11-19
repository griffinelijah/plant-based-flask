from flask import Flask, jsonify, g
import models

from resources.posts import posts

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
def after_request(response):
	#close connection to DB after every request
	g.db.close()
	return response

#default route
@app.route('/')
def hello():
	return 'Hello'


app.register_blueprint(posts, url_prefix='/api/v1/posts')

if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)