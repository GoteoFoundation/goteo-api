# -*- coding: utf-8 -*-

from flask import Flask
from flask_restful_swagger import swagger
from flask.ext.restful import Api
from flask.ext.restful.utils import cors
from flask.ext.sqlalchemy import SQLAlchemy

from config import config


# DB class
#app = Flask(__name__)
app = Flask(__name__, static_url_path="")
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

#Add CORS wide config
api.decorators=[cors.crossdomain(origin='*')]

db = SQLAlchemy(app)

