"""Config"""
import os
import string
import random


PACKAGE_ROOT = os.path.dirname(__file__)
MODEL_FILE = PACKAGE_ROOT + '/model/model.yaml'


class Config(object):
    """Flask app configuration super class."""
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    try:
        SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    except KeyError:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///'+PACKAGE_ROOT+'/../pmaapi.db'


class ProductionConfig(Config):
    """Flask app production configuration."""
    DEBUG = False


class StagingConfig(Config):
    """Flask app staging configuration."""
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    """Flask app development configuration."""
    DEVELOPMENT = True
    DEBUG = True


class TestConfig(Config):
    """Flask app test configuration."""
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False


def sk_generator(size=24, chars=string.ascii_letters + string.digits):
    """Secret key generator."""
    return ''.join(random.choice(chars) for _ in range(size))
