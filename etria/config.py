import os


class Config(object):
    DEBUG = False
    TESTING = False
    ASSETS_DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'development-secret-app-key'
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'uploads'

    # Database Settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Mail Settings
    MAIL_DEFAULT_SENDER = os.environ['EMAIL_SENDER']
    MAIL_SERVER = os.environ['EMAIL_SERVER']
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEBUG = False
    MAIL_USERNAME = os.environ['EMAIL_USER']
    MAIL_PASSWORD = os.environ['EMAIL_PASSWORD']


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    ASSETS_DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    ASSETS_DEBUG = True


class TestingConfig(Config):
    TESTING = True
