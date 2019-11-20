import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

posts = Blueprint('posts', 'posts')

#basic index route to display all created posts
@posts.route('/', methods=['GET'])
def post_index():
	try:
		posts = [model_to_dict(posts) for posts in models.Post.select()]
		return jsonify(data=posts, status={'code': 200, 'message': 'Successfully got all resources'}), 200
	except models.DoesNotExist:
		return jsonify(data={}, status={'code': 401, 'message': 'Error getting resources'})

#this route will show only posts created by the currently logged in user
@posts.route('/myPosts', methods=['GET'])
def current_users_posts():
	try:# look for all posts that have a user id that matches the currently logged in users id
		this_users_post_instances = models.Post.select().where(models.Post.user_id == current_user.id)
		#turn all posts found to be belong to current_user to arr of dicts
		this_users_post_dicts = [model_to_dict(post) for post in this_users_post_instances]
		return jsonify(data=this_users_post_dicts, status={'code': 200, 'message': 'Successfully retreived all of your posts'})
	except models.DoesNotExist:
		return jsonify(data={}, status={'code': 401, 'message': 'Error getting posts'}), 401

#route that let's you create a new post
@posts.route('/', methods=['POST'])
def create_post():
		#this route will let you create a post
		payload = request.get_json()
		#payload contents will create new post
		post = models.Post.create(
			user=current_user.id,
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


#route to update an existing post
@posts.route('/<id>', methods=['PUT'])
def update_post(id):
	payload = request.get_json()
	post = models.Post.get_by_id(id)

	#first we check to make sure the post belongs to the user by matching their id's
	if(post.user.id == current_user.id):
		models.Post.update(**payload)
		post.save()
		post_dict = model_to_dict(post)

		#remove password from user object before returning 
		post_dict['user'].pop('password')
		return jsonify(data=post_dict, status={'code': 200, 'message': 'post succesfully updated'}), 200

		#if they do not we will display a message stating you must be the owner of the post to update it
	else: return jsonify(data='Forbidden', status={'code': 403, 'message': 'You must be the owner of this post to update it'}), 403

	return jsonify(data=post_dict, status={'code': 200, 'message': 'post succesfully updated'}), 200

#route to delete a single post
@posts.route('/<id>', methods=['DELETE'])
def delete_post(id):
	#find post to delete by it's id
	post_to_delete = models.Post.get_by_id(id)
	#if the current_user id does not match the post owner's id do not allow deletion
	if post_to_delete.user.id != current_user.id:
		return jsonify(data='Forbidden', status={'code': 403, 'message': 'You must be the owner of this post to delete it'}), 403

	#else if they do match delete the post 
	else:
		post_to_delete.delete_instance()
	return jsonify(data={}, status={'code':200, 'message': 'resource succesfully deleted'})















