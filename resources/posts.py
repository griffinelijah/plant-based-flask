import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict

posts = Blueprint('posts', 'posts')

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