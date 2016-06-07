# -*- coding: utf-8 -*-
"""
    goteoapi
    ~~~~~~~~
    goteoapi main application package
"""
import time
from flask import Flask
from flask.ext.restful import Api
from flasgger import Swagger
from flask.ext.sqlalchemy import SQLAlchemy


def debug_time(func):
    def new_f(*args, **kwargs):
        time_start = time.time()
        res = func(*args, **kwargs)
        total_time = time.time() - time_start
        app.logger.debug('Time ' + func.__name__ + ': ' + str(total_time))
        return res
    return new_f

# DB class
#app = Flask(__name__)
app = Flask(__name__, static_url_path="")
app.config.from_pyfile('config.py')
# Custom config override
# From file
app.config.from_pyfile('../config.py', silent=True)
# From envvars
app.config.from_envvar('GOTEO_API_CONFIG_FILE', silent=True)

app.debug = bool(app.config['DEBUG'])
app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DB_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_POOL_TIMEOUT'] = 5
#app.config['SQLALCHEMY_POOL_SIZE'] = 30
if app.debug:
    app.config['SQLALCHEMY_ECHO'] = True

if 'CACHE' not in app.config:
    app.config['CACHE'] = {}

for i in app.config:
    if i.startswith('CACHE_'):
        app.config['CACHE'][i] = app.config[i]

if 'REDIS_URL' in app.config and 'CACHE_KEY_PREFIX' not in app.config['CACHE']:
    app.config['CACHE']['CACHE_KEY_PREFIX'] = 'Cacher/'

if 'CACHING' not in app.config:
    app.config['CACHING'] = False
    if 'CACHE_TYPE' in app.config['CACHE']:
        if app.config['CACHE']['CACHE_TYPE'] != 'null':
            app.config['CACHING'] = True

# print(app.config['CACHE'])

# Secret key
app.secret_key = app.config['SECRET_KEY']

db = SQLAlchemy(app)

# DEBUG
if app.debug:
    db.session.query = debug_time(db.session.query)
else:
    # loggin errors to a file if not debugging
    import logging
    import os
    f = os.path.dirname(os.path.realpath(__file__)) + '/errors.log'
    logging.basicConfig(filename=f, level=logging.ERROR)
    # handler = logging.FileHandler(f)
    # # handler.setLevel(logging.WARNING)
    # handler.setLevel(logging.ERROR)
    # app.logger.addHandler(handler)

# Swagger auto-yaml specification

# api = swagger.docs(Api(app), apiVersion=app.config['VERSION'], description=app.config['DESCRIPTION'])
# config your API specs
# you can define multiple specs in the case your api has multiple versions
# ommit configs to get the default (all views exposed in /spec url)
# rule_filter is a callable that receives "Rule" object and
#   returns a boolean to filter in only desired views

app.config['SWAGGER'] = {
    "swagger_version": "2.0",
    "basePath": app.config['BASE_PATH'],
    # headers are optional, the following are default
    "headers": [
        # ('Access-Control-Allow-Origin', '*'),
        # ('Access-Control-Allow-Headers', "Authorization, Content-Type"),
        # ('Access-Control-Expose-Headers', "Authorization"),
        # ('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE, OPTIONS"),
        # ('Access-Control-Allow-Credentials', "true"),
        # ('Access-Control-Max-Age', 60 * 60 * 24 * 20),
    ],
    # another optional settings
    # "subdomain": "docs.mysite,com",
    # specs are also optional if not set /spec is registered exposing all views
    "specs": [
        {
            "version": app.config['VERSION'],
            "title": app.config['DESCRIPTION'],
            "description": app.config['DESCRIPTION'],
            "endpoint": 'spec',
            "route": '/spec',

            # rule_filter is optional
            # it is a callable to filter the views to extract

            # "rule_filter": lambda rule: rule.endpoint.startswith(
            #    'should_be_v1_only'
            # )
        }
    ],
    # "static_url_path": "/apidocs",
    "test": 'text',
    "securityDefinitions": {
        # TODO: include oauth specification (login html screen must be generated)
        # "petstore_auth": {
        #     "type": "oauth2",
        #     "authorizationUrl": "/oauth/dialog",
        #     "flow": "implicit",
        #     "scopes": {
        #         "read:public": "Public content"
        #     }
        # },
        "basic": {
            "type": "basic"
        }
    }
}

Swagger(app)

api = Api(app)
