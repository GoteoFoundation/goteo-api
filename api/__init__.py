# -*- coding: utf-8 -*-

from flask import Flask
from flask_restful_swagger import swagger
from flask.ext.restful import Api
from flask.ext.sqlalchemy import SQLAlchemy

from config import config


# DB class
#app = Flask(__name__)
app = Flask(__name__, static_url_path="")
# Read debug status from config
if hasattr(config, 'debug'):
    app.debug = bool(config.debug)
    app.config['DEBUG'] = bool(config.debug)
    if app.debug:
        app.config['SQLALCHEMY_ECHO'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URI
#app.config['SQLALCHEMY_POOL_TIMEOUT'] = 5
#app.config['SQLALCHEMY_POOL_SIZE'] = 30
app.config['REDIS_URL'] = config.REDIS_URI
if hasattr(config, 'cache'):
    if 'CACHE_TYPE' in config.cache and config.cache['CACHE_TYPE'] == 'redis':
        if 'CACHE_KEY_PREFIX' not in config.cache:
            config.cache['CACHE_KEY_PREFIX'] = 'Cacher/'

    for i in config.cache:
        if i.startswith('CACHE_'):
            app.config[i] = config.cache[i]


#api = Api(app)

db = SQLAlchemy(app)

# DEBUG
if config.debug:
    from .decorators import debug_time
    db.session.query = debug_time(db.session.query)


api = swagger.docs(Api(app), apiVersion=config.version, description=config.description)
