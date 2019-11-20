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

#route to show individual comment
@comments.route('/<id>', methods=['GET'])
def get_one_comment(id):
	#retrieve comment by their id 
	comment = models.Comment.get_by_id(id)
	#turn to a dict
	comment_dict = model_to_dict(comment)
	return jsonify(data=comment_dict, status={'code': 201, 'message': 'successfully retrieved comment'})

#route to update an exising comment
@comments.route('/<id>', methods=['PUT'])
def update_comment(id):
	payload = request.get_json()
	#this query is to find a comment matching the id and update it with the info from the payload
	query = models.Comment.update(**payload).where(models.Comment.id == id)
	query.execute()
	#returns object as dictionary
	comment = models.Comment.get_by_id(id)
	comment_dict = model_to_dict(comment)
	return jsonify(data=comment_dict, status={'code': 200, 'message': 'Successfully updated comment'})

#route to delete individual comment
@comments.route('/<id>', methods=['DELETE'])
def delete_comment(id):
	#this will find the comment matching the id and delete it from the db
	query = models.Comment.delete().where(models.Comment.id == id)
	query.execute()
	return jsonify(data={}, status={'code': 200, 'message': 'Successfully deleted comment'})












