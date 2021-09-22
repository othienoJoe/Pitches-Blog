from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from . import login_manager

# categories table
class Category(db.Model):
	__tablename__ = 'categories'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	picture_path = db.Column(db.String(64))
	post = db.relationship('Post', backref='category', lazy='dynamic')

	# get all categories
	@staticmethod
	def get_all_categories():
			return Category.query.all()

	# save category
	def save_category(self):
			db.session.add(self)
			db.session.commit()

	def __repr__(self):
			return '<Category %r>' % self.name

# Roles table
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

# Monitor likes
class Like(db.Model):
	__tablename__ = 'likes'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

	# Saving likes to database
	def save_like(self):
			db.session.add(self)
			db.session.commit()

	# get all likes related to a single post
	@classmethod
	def get_likes(cls, post_id):
			likes = Like.query.filter_by(post_id=post_id).all()
			return likes

	# get like author details from author id
	@classmethod
	def get_like_author(cls, user_id):
			author = User.query.filter_by(id=user_id).first()
			return author


# A table for posts
class Post(db.Model):
	__tablename__ = 'posts'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(64))
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
	body = db.Column(db.Text)
	slug = db.Column(db.String(64), unique=True)
	picture_path = db.Column(db.String(64))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	like = db.relationship('Like', backref='post', lazy='dynamic')
	dislike = db.relationship('Dislike', backref='post', lazy='dynamic')
	comment = db.relationship('Comment', backref='post', lazy='dynamic')

	# gets posts by category
	@classmethod
	def get_posts_by_category(cls, category_id):
		return cls.query.filter_by(category_id=category_id).order_by(cls.timestamp.desc())

	# gets posts by author
	@classmethod
	def get_posts_by_author(cls, user_id):
		return cls.query.filter_by(user_id=user_id).order_by(cls.timestamp.desc())

	# save post
	def save_post(self):
		db.session.add(self)
		db.session.commit()


# Users' table
class User(UserMixin, db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64))
	username = db.Column(db.String(64), unique=True, index=True)
	email = db.Column(db.String(64), unique=True, index=True)
	password_hash = db.Column(db.String(128))

	about_me = db.Column(db.Text())
	profile_image = db.Column(db.String(64))
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	member_since = db.Column(db.DateTime(), default=datetime.utcnow)
	post = db.relationship('Post', backref='user', lazy="dynamic")

	@property
	def password(self):
			raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
			self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
			return check_password_hash(self.password_hash, password)

	# Searching and checking if the User Email exists
	@staticmethod
	def get_user_by_email(email):
			return User.query.filter_by(email=email).first()

	# Searching and checking if the User Username exists
	@staticmethod
	def get_user_by_username(username):
			return User.query.filter_by(username=username).first()

	@login_manager.user_loader
	def load_user(user_id):
			return User.query.get(int(user_id))

	def __repr__(self):
			return '<User %r>' % self.username


# A comments table
class Comment(db.Model):
	__tablename__ = 'comments'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
	body = db.Column(db.Text)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

	# save comment to database
	def save_comment(self):
			db.session.add(self)
			db.session.commit()

	# get all comments related to a single post
	@classmethod
	def get_comments(cls, post_id):
			comments = Comment.query.filter_by(post_id=post_id).all()
			return comments

	# get comment author details from author id
	@classmethod
	def get_comment_author(cls, user_id):
		author = User.query.filter_by(id=user_id).first()
		return author


# Saving the dislikes
class Dislike(db.Model):
	__tablename__ = 'dislikes'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

	# save like to database
	def save_dislike(self):
			db.session.add(self)
			db.session.commit()

	# get all likes related to a single post
	@classmethod
	def get_dislikes(cls, post_id):
			dislikes = Dislike.query.filter_by(post_id=post_id).all()
			return dislikes

	# get like author details from author id
	@classmethod
	def get_dislike_author(cls, user_id):
			author = User.query.filter_by(id=user_id).first()
			return author