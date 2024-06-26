"""Flask configuration."""
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """Base config which is inherited by all configurations."""
    SECRET_KEY = environ.get('SECRET_KEY')
    SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'


class ProdConfig(Config):
    """Production config."""
    FLASK_ENV = "production"
    FLASK_DEBUG = False
    DATABASE_URI = environ.get('PROD_DATABASE_URI')


class DevConfig(Config):
    """Development config."""
    FLASK_ENV = "development"
    FLASK_DEBUG = True
    DATABASE_SQLITE_URI = path.join(path.dirname(__file__), 'nlp-table-questioning.sqlite')
    DATABASE_HOST = environ.get('DEV_DATABASE_HOST')
    DATABASE_USER = environ.get('DEV_DATABASE_USER')
    DATABASE_PASS = environ.get('DEV_DATABASE_PASS')
    DATABASE_DB = environ.get('DEV_DATABASE_DB')