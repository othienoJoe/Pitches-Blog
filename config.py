import os

class Config:

	SECRET_KEY = os.environ.get('SECRET_KEY')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	UPLOADED_PICTURES = 'app/static/photos'

	# The Email Configurations
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
	MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

	# simplemde  configurations
	SIMPLEMDE_JS_IIFE = True
	SIMPLEMDE_USE_CDN = True

	@staticmethod
	def init_app(app):
		 pass

class TestConfig(Config):
	pass

class ProdConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
	pass

class DevConfig(Config):
	SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringa:1234@localhost/pitches'
	DEBUG = True

config_options = {
	'development' :DevConfig,
	'production' :ProdConfig,
	'test' : TestConfig
}
