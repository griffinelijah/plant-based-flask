from flask import Flask, jsonify, g
import models

from resources.posts import posts
from resources.users import users
from resources.comments import comments

from flask_login import LoginManager

DEBUG = True
PORT = 8000

#initialize instance of flask clasas
app = Flask(__name__)

#session secret, later on we will hide this for security
app.secret_key = 'shhhh'
#configuring the app to use loginmanager
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
	#this is where we find a matching user in the db to login
	try:
		return models.User.get(models.User.id == userid)
	except models.DoesNotExist:
		return None

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
app.register_blueprint(users, url_prefix='/api/v1/users')
app.register_blueprint(comments, url_prefix='/api/v1/comments')

if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)