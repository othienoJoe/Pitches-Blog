from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.core import BooleanField
from wtforms.fields.simple import PasswordField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Email, Length, EqualTo
from ..models import User
from wtforms import ValidationError

# TThe login form
class LoginForm(FlaskForm):
	"""
	This is the login form
	"""
	email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
	password = PasswordField('Password', validators=[Required()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Log In')

# The register form
class RegistrationForm(FlaskForm):
	"""
	This class defines the registration form
	"""
	name = StringField('Name', validators=[Required(), Length(1, 64)])
	email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
	username = StringField('Username', validators=[Required(), Length(1, 64)])
	password = PasswordField('Password', validators=[Required(), EqualTo('confirm_password', message='Passwords must match.')])
	confirm_password = PasswordField(
			'Confirm password', validators=[Required()])
	submit = SubmitField('Create Account')

	def check_email_exist(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('Email already registered. Please try to Login again')

	def check_username_exist(self, field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('This Username already exists.')
