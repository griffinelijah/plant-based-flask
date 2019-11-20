import models
from flask import request, jsonify, Blueprint
from playhouse.shortcuts import model_to_dict
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user

users = Blueprint('users', 'users')

#route to register a new user
@users.route('/register', methods=['POST'])
def register():
	payload = request.get_json()
	#lowercase all emails when registering to check against db and make sure email is not registered more than once
	payload['email'].lower()

	#first check to make sure email is not registered in the db
	try:
	#if email is registered in the db we want to send back and error and let them know the email has been previously registered
		models.User.get(models.User.email == payload['email'])
		return jsonify(data={}, status={'code': 401, 'message': 'A user with that email already exists'})

	#if the email has not been registered continue with registration
	except models.DoesNotExist:
		#this is encrypting the password from the payload to create a hash string
		payload['password'] = generate_password_hash(payload['password'])

		#create a user with the remaining payload info
		user = models.User.create(**payload)

		#after user registers we want to to automatically sign theem in
		login_user(user)
		#turn to dict and delete the users pw before returning the object
		user_dict = model_to_dict(user)
		del user_dict['password']
		return jsonify(data=user_dict, status={'code': 201, 'message': 'Succesfully registered user {}'.format(user_dict['email'])}),  201

#route to let users login
@users.route('/login', methods=['POST'])
def login():
	payload = request.get_json()
	#first look up user by their email
	try:#if match is found turn to dict and proceed
		user = models.User.get(models.User.email == payload['email'])
		user_dict = model_to_dict(user)
		#check if pw hash matches pw in db
		if(check_password_hash(user_dict['password'], payload['password'])):
			#if the pw matches the user in the db log them in
			login_user(user)
			#remove users password before returning the object
			del user_dict['password']
			return jsonify(data=user_dict, status={'code': 200, 'message': 'Succesfully logged in {}'.format(user_dict['email'])}), 200
		else: #if pw dose match user's pw in the db return error
			return jsonify(data={}, status={'code': 401, 'message': 'Username or Password is incorrect'}), 401

	except models.DoesNotExist:
		return jsonify(data={}, status={'code': 401, 'message': 'Username or Password is incorrect'}), 401

#route to let user logout
@users.route('/logout', methods=['GET'])
def logout():
	#logout user by their email
	email = model_to_dict(current_user)['email']
	logout_user()

	return jsonify(data={}, status={'code': 200, 'message': 'Succesfully logged out {}'.format(email)}), 200


















