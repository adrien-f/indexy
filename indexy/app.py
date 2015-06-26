import os
from flask import Flask, session
from flask.ext.cors import CORS
from flask.ext.redis import FlaskRedis

redis = FlaskRedis()


def create_app(config_file=None, config_object=None):
    """
    Bootstrap the flask application, registering blueprints, modules and other fun things.
    :param config_file: a python file containing key/values variables
    :param config_object: a python object (can be a dict) containing key/values variables
    :return: the app object
    """
    app = Flask(__name__, static_folder='public')

    # Configuration
    app.config.from_object('indexy.settings.BaseConfig')
    app.environment = os.getenv('INDEXY_ENV', 'dev')

    if config_file:
        app.config.from_pyfile(config_file)
    if config_object:
        app.config.update(**config_object)

    cors = CORS(app, resources={r'/api/*': {'origins': '*',}}, allow_headers='Content-Type')

    # Database, Migration, Login and models
    # from indexy.models import db, login_manager, migrate
    # db.init_app(app)
    # login_manager.init_app(app)
    # migrate.init_app(app, db)

    redis.init_app(app)

    from indexy.walker import walker
    walker.init_app(app)

    # from indexy.indexer import indexer
    # indexer.init_app(app)
    # indexer.build_index()

    from indexy.organizer import organizer
    organizer.init_app(app)
    organizer.organize(commit=True)

    # Blueprints
    from indexy.blueprints import TreeView
    TreeView.register(app)

    from indexy.utils import format_datetime, humanize, markdown_filter, number_of_files, number_of_folders, url_for_folder, get_icon
    app.jinja_env.filters['format_datetime'] = format_datetime
    app.jinja_env.filters['humanize'] = humanize
    app.jinja_env.filters['markdown'] = markdown_filter
    app.jinja_env.filters['number_of_files'] = number_of_files
    app.jinja_env.filters['number_of_folders'] = number_of_folders
    app.jinja_env.globals['url_for_folder'] = url_for_folder
    app.jinja_env.globals['get_icon'] = get_icon
    app.jinja_env.globals['walker'] = walker

    return app
