import datetime
from peewee import *
from flask_login import UserMixin

DATABASE = SqliteDatabase('plant_based.sqlite')

class User(UserMixin, Model):
	username = CharField(unique=True)
	email = CharField(unique=True)
	password = CharField()

	class Meta:
		database = DATABASE

class Comment(Model):
	user = ForeignKeyField(User, backref='comments')
	body = CharField()
	# post = ForeignKeyField(Post, backref='comments')

	class Meta:
		database = DATABASE


class Post(Model):
	# user = ForeignKeyField(User, backref='posts')
	comment = CharField() #this will change to a foreignkeyfield once comments are introduced
	title = CharField()
	description = CharField()
	image = CharField()
	created = DateTimeField(default=datetime.datetime.now)

	class Meta:
		database = DATABASE


def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User, Comment, Post], safe=True)
	print('TABLES CREATED')
	DATABASE.close()

