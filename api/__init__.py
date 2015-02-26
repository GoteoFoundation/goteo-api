# -*- coding: utf-8 -*-

from flask import Flask
from flask_restful_swagger import swagger
from flask.ext.restful import Api
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cache import Cache
from config import config

cache = Cache(config={'CACHE_TYPE': 'simple'})

# DB class
#app = Flask(__name__)
app = Flask(__name__, static_url_path="")
cache.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URI
app.config['SQLALCHEMY_ECHO'] = True
app.config['REDIS_URL'] = config.REDIS_URI
#app.config['SQLALCHEMY_POOL_TIMEOUT'] = 5
#app.config['SQLALCHEMY_POOL_SIZE'] = 30

#
# Read debug status from config
if hasattr(config, 'debug'):
    app.debug = bool(config.debug)
    app.config['DEBUG'] = bool(config.debug)


api = swagger.docs(Api(app), apiVersion=config.version, description=config.description)
#api = Api(app)

db = SQLAlchemy(app)


