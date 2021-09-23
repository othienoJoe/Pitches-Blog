from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,FileField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import Required,Email,Length,EqualTo
from ..models import User
from wtforms import ValidationError

class UpdateProfileForm(FlaskForm):
	name = StringField('Name', validators=[Required(), Length(1, 64)])
	username = StringField('Username', validators=[Required(), Length(1, 64)])
	email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
	about_me = TextAreaField('About me', validators=[Required(), Length(1, 100)])
	
	submit = SubmitField('Update Profile')
	
class CommentForm(FlaskForm):
	body = TextAreaField('Comment', validators=[Required()])
	submit = SubmitField('Submit')

class CategoryForm(FlaskForm):
	name = StringField('Category Name', validators=[Required(), Length(1, 64)])
	submit = SubmitField('Submit')
	