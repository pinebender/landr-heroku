# TODO: turn this section into __init__.py


from flask import Flask, render_template, request, redirect, url_for, session, flash

# model imports
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_pyfile('config.py')
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
	title = db.Column(db.String(80))
	body = db.Column(db.Text)
	value = db.Column(db.Integer)
	pub_date = db.Column(db.DateTime)
	complete = db.Column(db.Boolean)
	userid = db.Column(db.Integer, db.ForeignKey('user.id'))
	user = db.relationship('User', backref=db.backref('tasks', lazy='dynamic'))
	
	def __init__(self, title, body, user, value=None, pub_date=None):
		self.title = title
		self.body = body
		if value is None:
			value = 0;
		self.value = value
		if pub_date is None:
			pub_date = datetime.utcnow()
		self.pub_date = pub_date
		self.complete = False;
		self.user = user

	def __repr__(self):
		return '<Task %r>' % self.title


class Reward(db.Model):
	id = db.Column(db.Integer, primary_key=True)


# TODO: turn this section into views.py
@app.route('/')
def home():
	# if a session exists
	if session:
		user = User.query.get(session['userid'])	
		return render_template('home.html', username=user.username, points=user.points, tasks=user.tasks)
	# if no session, display default home page. TODO: convert to splash page
	else:
		return render_template('front.html')

@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
	if session:
		
		user = User.query.get(session['userid'])	
		
		if request.method == 'POST':
			if request.form['title']:
				# add task
				newtask = Task(request.form['title'], request.form['body'], user, request.form['value'])
				if newtask.value < 0 or newtask.value.isdigit() == False:
					newtask.value = 0
				db.session.add(newtask)
				db.session.commit()
				return redirect(url_for('tasks'))
		else:			
			
			return render_template('tasks.html', username=user.username, points=user.points, tasks=user.tasks)
	# if no session, display default home page. TODO: convert to splash page
	else:
		return redirect(url_for('home'))

@app.route('/deletetask', methods=['GET', 'POST'])
def deltask():
	if session:
		user = User.query.get(session['userid'])
		if request.method == 'POST':
			if request.form['deltaskid']:
				task = Task.query.get(request.form['deltaskid'])
				# change this to hide tasks, but leave them in the database
				db.session.delete(task)
				db.session.commit()
				return redirect(url_for('tasks'))
		else:			
			return render_template('tasks.html', username=user.username, points=user.points, tasks=user.tasks)
	else:
		return redirect(url_for('home'))

@app.route('/completetask', methods=['GET', 'POST'])
def completetask():
	if session:
		user = User.query.get(session['userid'])
		if request.method == 'POST':
			if request.form['comptaskid']:
				task = Task.query.get(request.form['comptaskid'])
				task.complete = True
				user.points += task.value
				db.session.commit()
				return redirect(url_for('tasks'))
		else:
			return render_template('tasks.html', username=user.username, points=user.points, tasks=user.tasks)
	else:
		return redirect(url_for('home'))




@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':

		# if a username was retrieved in POST
		if request.form['username']:
			
			#query database by username in lowercase
			user = User.query.filter_by(username = request.form['username'].lower()).first()
			
			#if matching user is found in database
			if user:
				# if the hashed password from POST matches the hash stored in the database, add userid to session and redirect
				if check_password_hash(user.password, request.form['password']):
					session['userid'] = user.id
					return redirect(url_for('home'))
				# if the hashed password does not match the hash in the database, flash an error.
				else:
					flash('Login failed. Please try again.')
					return render_template('login.html')
			# if user was not found in database, flash error
			else:
				flash('Login failed. Please try again.')
				return render_template('login.html')
	
	else:
		return render_template('login.html')

@app.route('/logout')
def logout():
	session.pop('userid', None)
	return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	# if post data exists
	if request.method == 'POST':
		usernm = request.form['username']
		pw = request.form['password']
		verify = request.form['verify']
		userquery = User.query.filter_by(username=usernm.lower()).first()
		
		# if query returns a user from database, check if it matches post data
		if userquery != None:
			# convert name data from POST to lowercase and check vs database (name also in lowercase)
			if usernm.lower() == userquery.username:
				flash("Username is already in use. Please choose another.")
				return redirect(url_for('register'))
		
		# if query does not return a name, check if form passwords match
		elif pw != verify:
			flash("Password doesn't match verification. Please try again.")
			return redirect(url_for('register'))
		
		# if passwords match, hash the password and store the user in database, username in lowercase
		elif pw == verify:
			pwhash = generate_password_hash(pw)
			
			newuser = User(usernm.lower(), pwhash)			
			db.session.add(newuser)
			
			newtask = Task("Your first task:", "Mark this as complete for 1 point!", newuser, 1)
			db.session.add(newtask)
			
			db.session.commit()
			session['userid'] = newuser.id
			return redirect(url_for('home'))
	
	# form view when no POST data
	else:
		return render_template('register.html')


if __name__ == '__main__':
	app.secret_key = 'ADSFKJASDFKJADSFJ' #temporary dev key
	app.run(host='0.0.0.0', debug=True)