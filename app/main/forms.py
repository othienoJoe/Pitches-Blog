from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,FileField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import Required,Email,Length,EqualTo

class UpdateProfileForm(FlaskForm):
	name = StringField('Name', validators=[Required(), Length(1, 64)])
	username = StringField('Username', validators=[Required(), Length(1, 64)])
	email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
	about_me = TextAreaField('About me', validators=[Required(), Length(1, 100)])
	
	submit = SubmitField('Update Profile')
	