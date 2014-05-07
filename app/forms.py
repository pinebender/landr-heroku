from flask_wtf import Form
from wtforms import TextField, IntegerField, BooleanField, PasswordField, HiddenField, validators 
from wtforms import TextAreaField
from wtforms.validators import Required, EqualTo, Optional, Length, Email, NumberRange


# WTForms
class RegistrationForm(Form):
	username = TextField('Username', [validators.Length(min=4, max=25, message=("Username must be between 4 and 25 characters in length.")), validators.Required(), ])
	#email = TextField('Email Address', [validators.Length(min=6, max=35), Required()])
	password = PasswordField('Password', [validators.Length(min=6, message=("Password must be at least 6 characters long.")), validators.Required(), validators.EqualTo('verify', message='Password does not match confirmation.')])
	verify = PasswordField('Confirm Password')

class LoginForm(Form):
	username = TextField('Username')
	password = PasswordField('Password')

class TaskForm(Form):
	title = TextAreaField('Title', [validators.Required(), validators.Length(max=300, message="Please enter a title between 0 and 300 characters in length")])
	value = IntegerField('Value', [validators.NumberRange(min=0, max=1000, message="Please enter a non-negative number between 0 and 1000")])

class RewardForm(Form):
	title = TextAreaField('Title', [validators.Required(), validators.Length(max=300, message="Please enter a title between 0 and 300 characters in length")])
	cost = IntegerField('Cost', [validators.NumberRange(min=0, max=1000, message="Please enter a non-negative number between 0 and 1000")])

class TaskIdForm(Form):
	taskid = HiddenField('TaskID', [validators.NumberRange(min=0)])
	referpage = HiddenField('RefPage')

class RewardIdForm(Form):
	rewardid = HiddenField('RewardID', [validators.NumberRange(min=0)])
	referpage = HiddenField('RefPage')
