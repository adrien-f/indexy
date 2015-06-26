import os


class BaseConfig(object):
    """File based configuration object."""

    #: Secret key for securing cookies.
    #: Generate one with `openssl rand -base64 64`
    SECRET_KEY = '8TvFtAWMS5KI2DRcqVjO5+nmkJxe9H1T9MLJvD39652YHe0uLRkarpCbR8m/tfi+Z2Of15F9fGVl27PGhNvalA=='

    #: Application absolute path
    APP_DIR = os.path.abspath(os.path.dirname(__file__))

    #: Project root
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))

    #: Turn on debug mode by environment
    DEBUG = os.getenv('DEBUG', True)

    #: Default SQLAlchemy database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + PROJECT_ROOT + '/indexy.sqlite'

    #: Turn on debug mode for SQLAlchemy (prints out queries)
    SQLALCHEMY_ECHO = os.getenv('DEBUG', False)

    #: HTTP scheme (can be http, https, etc...)
    HTTP_SCHEME = 'http'

    REDIS_URL = 'redis://192.168.33.10:6379/0'
