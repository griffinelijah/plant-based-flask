import os
import datetime
from peewee import *
from flask_login import UserMixin
from playhouse.db_url import connect


if 'ON_HEROKU' in os.environ:
	DATABASE  = connect(os.environ.get('DATABASE_URL'))

else:
	DATABASE = SqliteDatabase('plant_based.sqlite')

class User(UserMixin, Model):
	username = CharField(unique=True)
	email = CharField(unique=True)
	password = CharField()

	class Meta:
		database = DATABASE

class Post(Model):
	user = ForeignKeyField(User, backref='posts')
	title = CharField()
	description = CharField()
	image = CharField()
	created = DateTimeField(default=datetime.datetime.now)

	class Meta:
		database = DATABASE
		
class Comment(Model):
	user = ForeignKeyField(User, backref='comments')
	body = CharField()
	post = ForeignKeyField(Post, db_column='post', backref='comments')

	class Meta:
		database = DATABASE



def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User, Post, Comment], safe=True)
	print('TABLES CREATED')
	DATABASE.close()

