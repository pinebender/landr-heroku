
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
#for ordering queries in descending fashion
from app import app

db = SQLAlchemy(app)
# TODO: turn this section into models.py
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True)
	password = db.Column(db.String(80))
	points = db.Column(db.Integer)

	def __init__(self, username, password):
		self.username = username
		self.password = password
		self.points = 0

	def __repr__(self):
		return '<User %r>' % self.username

''' Sample functions for password hashing
	def set_password(self, password):
		self.pw_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.pw_hash, password)
'''

class Task(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.Text)
	body = db.Column(db.Text)
	value = db.Column(db.Integer)
	dateadded = db.Column(db.DateTime)
	datedue = db.Column(db.DateTime)
	complete = db.Column(db.Boolean)
	datecomplete = db.Column(db.DateTime)
	userid = db.Column(db.Integer, db.ForeignKey('user.id'))
	user = db.relationship('User', backref=db.backref('tasks', lazy='dynamic'))
	
	def __init__(self, title, user, body=None, value=None, dateadded=None, datedue=None):
		self.title = title
		if body is None:
			body = 0
		self.body = None
		if value is None:
			value = 0;
		self.value = value
		if dateadded is None:
			dateadded = datetime.utcnow()
		self.dateadded = dateadded
		if datedue is None:
			datedue = None #in html show as "Any time" or somesuch if None
		self.datedue = datedue
		self.complete = False;
		self.datecomplete = None #in html only show on Completed Tasks table
		self.user = user

	def __repr__(self):
		return '<Task %r>' % self.title


class Reward(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.Text)
	body = db.Column(db.Text)
	cost = db.Column(db.Integer)
	dateadded = db.Column(db.DateTime)
	redeemed = db.Column(db.Boolean)
	dateredeemed = db.Column(db.DateTime)
	# add self.expires = db.Column(db.DateTime)
	userid = db.Column(db.Integer, db.ForeignKey('user.id'))
	user = db.relationship('User', backref=db.backref('rewards', lazy='dynamic'))


	def __init__(self, title, user, body=None, cost=None, dateadded=None):
		self.title = title
		if body is None:
			body = 0
		self.body = body
		if cost is None:
			cost = 0
		self.cost = cost
		if dateadded is None:
			dateadded = datetime.utcnow()
		self.dateadded = dateadded
		self.redeemed = False
		self.dateredeemed = None # if None, don't display in template
		self.user = user

	def __repr__(self):
		return '<Reward %r>' % self.title