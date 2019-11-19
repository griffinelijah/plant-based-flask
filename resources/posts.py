import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict

posts = Blueprint('posts', 'posts')

#basic index route to display all created posts
@posts.route('/', methods=['GET'])
def post_index():
	try:
		posts = [model_to_dict(posts) for posts in models.Post.select()]
		return jsonify(data=posts, status={'code': 200, 'message': 'Successfully got all resources'}), 200
	except models.DoesNotExist:
		return jsonify(data={}, status={'code': 401, 'message': 'Error getting resources'})

@posts.route('/', methods=['POST'])
def create_post():
		#this route will let you create a post
		payload = request.get_json()
		#payload contents will create new post
		post = models.Post.create(
			# user=current_user.id,
			comment=payload['comment'],
			title=payload['title'],
			description=payload['description'],
			image=payload['image']
		)
		#must be turned into a dict before returning the json object
		post_dict = model_to_dict(post)
		return jsonify(data=post_dict, status={'code': 201, 'message': 'sucessfully created post'}), 201

#route to retrieve a single post
@posts.route('/<id>', methods=['GET'])
def get_one_post(id):
	post = models.Post.get_by_id(id)
	post_dict = model_to_dict(post)
	return jsonify(data=post_dict, status={'code': 201, 'message': 'successfully retrieved postt'})