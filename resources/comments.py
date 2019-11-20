import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

comments = Blueprint('comments', 'comments')

#route to create a comment
@comments.route('/', methods=['POST'])
def create_comment():
	#payload will contain info to create a comment
	payload = request.get_json()
	#create new comment from payload info
	comment = models.Comment.create(
		#this will tie a comment to whoever the logged in user is
		user=current_user.id,
		body=payload['body']
	)
	#must be turned to a dict before returning
	comment_dict = model_to_dict(comment)
	return jsonify(data=comment_dict, status={'code': 201, 'status': 'Successfully created comment'}), 201

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
	#query to find comment matching the id
	comment = models.Comment.get_by_id(id)
	#before updating comment make sure user's id matching the logged in user id
	if(comment.user.id == current_user.id):
		models.Comment.update(**payload)
		comment.save()
		#returns object as dictionary
		comment_dict = model_to_dict(comment)
		comment_dict['user'].pop('password')
		return jsonify(data=comment_dict, status={'code': 200, 'message': 'Successfully updated comment'})
	#else if the do not 'own' this comment display error stating they must own it to update it
	else:
		return jsonify(data='Forbidden', status={'code': 403, 'message': 'You must be the owner of this comment to delete it'}), 403

	return jsonify(data=comment_dict, status={'code': 200, 'message': 'Successfully updated comment'})

#route to delete individual comment
@comments.route('/<id>', methods=['DELETE'])
def delete_comment(id):
	#this will find the comment matching the id and delete it from the db
	query = models.Comment.delete().where(models.Comment.id == id)
	query.execute()
	return jsonify(data={}, status={'code': 200, 'message': 'Successfully deleted comment'})












