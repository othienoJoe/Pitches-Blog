from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from . import auth
from ..models import User
from .forms import LoginForm, RegistrationForm
from .. import db
from ..email import mail_message

# To register a new user
@auth.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		if User.get_user_by_email(form.email.data):
				flash('Email already registered 😥', 'warning')
				return redirect(url_for('auth.register'))
		elif User.get_user_by_username(form.username.data):
				flash('Username already registered 😥', 'warning')
				return redirect(url_for('auth.register'))
		# To check if password is greater than 8 characters
		elif len(form.password.data) < 8:
				flash('Password should be at least 8 characters long 😥', 'warning')
				return redirect(url_for('auth.register'))
		else:
				user = User(email=form.email.data,
										username=form.username.data, password=form.password.data,name=form.name.data)
				db.session.add(user)
				db.session.commit()
				flash('User Account created successfully!', 'success')
				return redirect(url_for('auth.login'))
	title = "Create New Account"
	return render_template('auth/register.html', title=title, registration_form=form)

# To login user
@auth.route('/login', methods=['GET', 'POST'])
def login():
	login_form = LoginForm()
	if login_form.validate_on_submit():
		user = User.query.filter_by(email=login_form.email.data).first()
		if user is not None and user.verify_password(login_form.password.data):
				login_user(user, login_form.remember.data)
				return redirect(request.args.get('next') or url_for('main.profile', username=user.username))

		flash('Invalid email or Password')

	title = "Login to your account"
	return render_template('auth/login.html', login_form=login_form, title=title)

# To log out user
@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been successfully logged out')
	return redirect(url_for("main.index"))