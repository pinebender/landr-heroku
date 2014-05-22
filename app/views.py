from flask import render_template, request, redirect, url_for, session, flash
from datetime import datetime
from app import app
from models import User, Task, Reward, db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc
from forms import RegistrationForm, LoginForm, TaskForm, RewardForm, TaskIdForm, RewardIdForm, TaskUpdateForm, RewardUpdateForm


# TODO: turn this section into views.py
@app.route('/')
def front():
	if 'userid' in session:
		return redirect(url_for('tasks'))
	return render_template('front.html', loginform=LoginForm(), regform=RegistrationForm(), containerclass="frontcontainer")

@app.route('/home')
def home():
	# if a session exists
	if 'userid' in session:
		user = User.query.get_or_404(session['userid'])
		tasks = user.tasks.filter(Task.complete ==False).order_by(desc(Task.dateadded)).all()	
		return render_template('home.html', username=user.username, points=user.points, tasks=tasks, containerclass="homecontainer")
	# if no session, display default home page. TODO: convert to splash page
	else:
		return redirect(url_for('front'))

@app.route('/tasks', methods=['GET', 'POST']) #TODO: modify this to validate with WTForms
def tasks():
	
	if 'userid' in session:	
		user = User.query.get_or_404(session['userid'])	
		
		if request.method == 'POST':
			form = TaskForm(request.form)
			if form.validate():
				newtask = Task(form.title.data, user, None, form.value.data)
				db.session.add(newtask)
				db.session.commit()
				return redirect(url_for('tasks'))
			else:
				tasks = user.tasks.filter(Task.complete == False).order_by(desc(Task.dateadded)).all()	
				return render_template('tasks.html', username=user.username, points=user.points, tasks=tasks, form=form, idform=TaskIdForm(), updateform=TaskUpdateForm(), containerclass="listcontainer")

		else:
			tasks = user.tasks.filter(Task.complete == False).order_by(desc(Task.dateadded)).all()			
			return render_template('tasks.html', username=user.username, points=user.points, tasks=tasks, form=TaskForm(), idform=TaskIdForm(), updateform=TaskUpdateForm(), containerclass="listcontainer")
	# if no session, display default home page. TODO: convert to splash page
	else:
		return redirect(url_for('front'))

@app.route('/completed', methods=['GET', 'POST'])
def completed():
	if 'userid' in session:	
		user = User.query.get_or_404(session['userid'])	
		comptasks = user.tasks.filter(Task.complete == True).order_by(desc(Task.datecomplete)).all()			
		return render_template('completed.html', username=user.username, points=user.points, comptasks=comptasks, idform=TaskIdForm(), containerclass="listcontainer")
	# if no session, display default home page. TODO: convert to splash page
	else:
		return redirect(url_for('front'))

@app.route('/taskupdate', methods=['GET', 'POST']) # instead of using a separate page for task details, convert this into an update function
def taskupdate():
	if 'userid' in session:
		user = User.query.get_or_404(session['userid'])
		if request.method == 'POST':
			updateform = TaskUpdateForm(request.form)
			if updateform.validate():
				task = Task.query.get_or_404(updateform.taskid.data)
				if task.userid == user.id:
					# update fields
					task.title = updateform.title.data
					task.value = updateform.value.data
					#task.datedue = updateform.datedue.data
					db.session.commit()
				return redirect(url_for('tasks'))
			else:
				tasks = user.tasks.filter(Task.complete == False).order_by(desc(Task.dateadded)).all()
				return render_template('tasks.html', username=user.username, points=user.points, tasks=tasks, form=TaskForm(), idform=TaskIdForm(), updateform=updateform, containerclass="listcontainer" )
		else:
			return redirect(url_for('tasks'))
	else:
		return redirect(url_for('front'))

@app.route('/deletetask', methods=['GET', 'POST'])
def deltask():
	if 'userid' in session:
		user = User.query.get_or_404(session['userid'])
		if request.method == 'POST':
			form = TaskIdForm(request.form)
			if form.validate():
				task = Task.query.get_or_404(form.taskid.data)
				# change this to hide tasks, but leave them in the database?
				if task.userid == user.id:
					db.session.delete(task)
					db.session.commit()
			if form.referpage.data == "completed":
				return redirect(url_for('completed'))
			else:
				return redirect(url_for('tasks'))
		else:			
			return redirect(url_for('tasks'))
	else:
		return redirect(url_for('front'))

@app.route('/completetask', methods=['GET', 'POST'])
def completetask():
	if 'userid' in session:
		user = User.query.get_or_404(session['userid'])
		if request.method == 'POST':
			form = TaskIdForm(request.form)
			if form.validate():
				task = Task.query.get_or_404(form.taskid.data)
				task.complete = True
				task.datecomplete = datetime.utcnow()
				user.points += task.value
				db.session.commit()
			return redirect(url_for('tasks'))
		else:
			return redirect(url_for('tasks'))
	else:
		return redirect(url_for('front'))


@app.route('/rewards', methods=['GET', 'POST'])
def rewards():
	if 'userid' in session:	
		user = User.query.get_or_404(session['userid'])	
		
		if request.method == 'POST':
			form = RewardForm(request.form)
			if form.validate():
				print form.cost.data
				newreward = Reward(form.title.data, user, None, form.cost.data)
				db.session.add(newreward)
				db.session.commit()
				return redirect(url_for('rewards'))
			else:
				rewards = user.rewards.filter(Reward.redeemed == False).order_by(desc(Reward.dateadded)).all()	
				return render_template('rewards.html', username=user.username, points=user.points, rewards=rewards, form=form, idform=RewardIdForm(), updateform=RewardUpdateForm(), containerclass="rewardcontainer")

		else:
			rewards = user.rewards.filter(Reward.redeemed == False).order_by(desc(Reward.dateadded)).all()			
			return render_template('rewards.html', username=user.username, points=user.points, rewards=rewards, form=RewardForm(), idform=RewardIdForm(), updateform=RewardUpdateForm(), containerclass="rewardcontainer")
	# if no session, display default home page. TODO: convert to splash page
	else:
		return redirect(url_for('front'))

@app.route('/redeemed', methods=['GET', 'POST'])
def redeemed():
	if 'userid' in session:	
		user = User.query.get_or_404(session['userid'])	
		redeemed = user.rewards.filter(Reward.redeemed == True).order_by(desc(Reward.dateredeemed)).all()			
		return render_template('redeemed.html', username=user.username, points=user.points, redeemed=redeemed, idform=RewardIdForm(), containerclass="rewardcontainer")
	# if no session, display default home page. TODO: convert to splash page
	else:
		return redirect(url_for('front'))

@app.route('/rewardupdate', methods=['GET', 'POST']) # instead of using a separate page for task details, convert this into an update function
def rewardupdate():
	if 'userid' in session:
		user = User.query.get_or_404(session['userid'])
		if request.method == 'POST':
			updateform = RewardUpdateForm(request.form)
			if updateform.validate():
				reward = Reward.query.get_or_404(updateform.rewardid.data)
				if reward.userid == user.id:
					# update fields
					reward.title = updateform.title.data
					reward.cost = updateform.cost.data
					#task.datedue = updateform.datedue.data
					db.session.commit()
				return redirect(url_for('rewards'))
			else:
				rewards = user.rewards.filter(Reward.redeemed == False).order_by(desc(Reward.dateadded)).all()
				return render_template('rewards.html', username=user.username, points=user.points, rewards=rewards, form=RewardForm(), idform=RewardIdForm(), updateform=updateform, containerclass="rewardcontainer" )
		else:
			return redirect(url_for('rewards'))
	else:
		return redirect(url_for('front'))
	

@app.route('/redeem', methods=['GET', 'POST'])
def redeem():
	if 'userid' in session:
		user = User.query.get_or_404(session['userid'])
		if request.method == 'POST':
			form = RewardIdForm(request.form)
			if form.validate():
				reward = Reward.query.get_or_404(form.rewardid.data)
				reward.redeemed = True
				reward.dateredeemed = datetime.utcnow()
				user.points -= reward.cost
				db.session.commit()
			return redirect(url_for('rewards'))
		else:
			return redirect(url_for('rewards'))
	else:
		return redirect(url_for('front'))


@app.route('/deletereward', methods=['GET', 'POST'])
def deletereward():
	if 'userid' in session:
		user = User.query.get_or_404(session['userid'])
		if request.method == 'POST':
			form = RewardIdForm(request.form)
			if form.validate():
				reward = Reward.query.get_or_404(form.rewardid.data)
				# change this to hide tasks, but leave them in the database?
				if reward.userid == user.id:
					db.session.delete(reward)
					db.session.commit()
			if form.referpage.data == "redeemed":
				return redirect(url_for('redeemed'))
			else:
				return redirect(url_for('rewards'))
		else:			
			return redirect(url_for('rewards'))
	else:
		return redirect(url_for('front'))



@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		form = LoginForm(request.form)
		if form.validate():
			#query database by username in lowercase
			user = User.query.filter_by(username = form.username.data.lower()).first()
	
			#if matching user is found in database
			if user:
				# if the hashed password from POST matches the hash stored in the database, add userid to session and redirect
				if check_password_hash(user.password, form.password.data):
					session['userid'] = user.id
					return redirect(url_for('tasks'))
				else:
					form.password.errors.append("Login Failed. Please try again.")
					return render_template('front.html', loginform=form, regform=RegistrationForm(), containerclass="frontcontainer")
			# if user was not found in database or hashed password does not match, display error
			else:
				form.username.errors.append("Login Failed. Please try again.")
				return render_template('front.html', loginform=form, regform=RegistrationForm(), containerclass="frontcontainer")
	
	else:
		return redirect(url_for('tasks'))

@app.route('/logout')
def logout():
	session.pop('userid', None)
	return redirect(url_for('front'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	# if post data exists
	if request.method == 'POST':
		form = RegistrationForm(request.form)
		if form.validate():
			usernm = form.username.data
			pw = form.password.data
			verify = form.verify.data
			userquery = User.query.filter_by(username=usernm.lower()).first()
			
			# if query returns a user from database, check if it matches post data
			if userquery != None:
				# convert name data from POST to lowercase and check vs database (name also in lowercase)
				if usernm.lower() == userquery.username:
					#flash("Username is already in use. Please choose another.")
					form.username.errors.append("Username is already in use. Please choose another.")
					return render_template('front.html', regform=form, loginform=LoginForm(), containerclass="frontcontainer")
			
			# if query does not return a name, check if form passwords match
			elif pw != verify:
				#flash("Password doesn't match verification. Please try again.")
				form.password.errors.append("Password doesn't match verification. Please try again.")
				return render_template('front.html', regform=form, loginform=LoginForm(), containerclass="frontcontainer")
			
			# if passwords match, hash the password and store the user in database, username in lowercase
			elif pw == verify:
				pwhash = generate_password_hash(pw)
				
				newuser = User(usernm.lower(), pwhash)			
				db.session.add(newuser)
				
				newtask = Task("Welcome to List and Reward. Have a free point!", newuser, None, 1)
				db.session.add(newtask)

				newreward = Reward("Pat yourself on the back. You deserve it.", newuser, None, 1)
				db.session.add(newreward)
				
				db.session.commit()
				session['userid'] = newuser.id
				return redirect(url_for('tasks'))

		else:
			return render_template('front.html', regform=form, loginform=LoginForm(), containerclass="frontcontainer")
		
	# form view when no POST data
	else:
		return render_template('front.html', loginform=LoginForm(), regform=RegistrationForm(), containerclass="frontcontainer")