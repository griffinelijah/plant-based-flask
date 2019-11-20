import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict

comments = Blueprint('comments', 'comments')

#route to create a comment
@comments.route('/', methods=['POST'])
def create_comment():
	#payload will contain info to create a comment
	payload = request.get_json()
	#create new comment from payload info
	comment = models.Comment.create(**payload)
	#must be turned to a dict before returning
	comment_dict = model_to_dict(comment)
	return jsonify(data=comment_dict, status={'code': 201, 'status': 'Successfully created comment'})

