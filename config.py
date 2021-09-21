import os

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY')
	SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(Config):
	pass

class ProdConfig(Config):
	pass

class DevConfig(Config):
	DEBUG = True

config_options = {
	'development' :DevConfig,
	'production' :ProdConfig,
	'test' : TestConfig
}
