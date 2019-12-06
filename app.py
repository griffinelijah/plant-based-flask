import os
from flask import Flask, jsonify, g
from flask_cors import CORS
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
@login_manager.unauthorized_handler
def unauthorized():
	return jsonify(data={
			'error': 'user not logged in'
		}, status={
			'code': 401,
			'message': 'You must be logged in to access that resource'
		}), 401

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


CORS(posts, origins=['http://localhost:3000', 'https://plant-based-react.herokuapp.com'], supports_credentials=True)
CORS(users, origins=['http://localhost:3000', 'https://plant-based-react.herokuapp.com'], supports_credentials=True)
CORS(comments, origins=['http://localhost:3000','https://plant-based-react.herokuapp.com'], supports_credentials=True)



app.register_blueprint(posts, url_prefix='/api/v1/posts')
app.register_blueprint(users, url_prefix='/api/v1/users')
app.register_blueprint(comments, url_prefix='/api/v1/comments')

if 'ON_HEROKU' in os.environ: 
  print('\non heroku!')
  models.initialize()

if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)