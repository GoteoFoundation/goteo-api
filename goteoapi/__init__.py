# -*- coding: utf-8 -*-
"""
    goteoapi
    ~~~~~~~~
    goteoapi main application package
"""

from flask import Flask
from flask_restful_swagger import swagger
from flask.ext.restful import Api
from flask.ext.sqlalchemy import SQLAlchemy

# DB class
#app = Flask(__name__)
app = Flask(__name__, static_url_path="")
app.config.from_pyfile('config.py')
#Custom config override
app.config.from_pyfile('../config.py', silent=True)

app.debug = bool(app.config['DEBUG'])
app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DB_URI']
#app.config['SQLALCHEMY_POOL_TIMEOUT'] = 5
#app.config['SQLALCHEMY_POOL_SIZE'] = 30
if app.debug:
    app.config['SQLALCHEMY_ECHO'] = True

app.config['CACHING'] = False
if 'CACHE_TYPE' in app.config['CACHE']:
    if app.config['CACHE']['CACHE_TYPE'] != 'null':
        app.config['CACHING'] = True
    if app.config['CACHE']['CACHE_TYPE'] == 'redis':
        if 'CACHE_KEY_PREFIX' not in app.config['CACHE']:
            app.config['CACHE']['CACHE_KEY_PREFIX'] = 'Cacher/'

for i in app.config['CACHE']:
    if i.startswith('CACHE_'):
        app.config[i] = app.config['CACHE'][i]

db = SQLAlchemy(app)

# DEBUG
if app.debug:
    from .decorators import debug_time
    db.session.query = debug_time(db.session.query)
else:
    # loggin errors to a file if not debugging
    import logging, os
    logging.basicConfig(filename='error.log',level=logging.ERROR)
    # handler = logging.FileHandler(os.path.dirname(os.path.realpath(__file__)) + '/errors.log')
    # # handler.setLevel(logging.WARNING)
    # handler.setLevel(logging.ERROR)
    # app.logger.addHandler(handler)

#api = Api(app)
api = swagger.docs(Api(app), apiVersion=app.config['VERSION'], description=app.config['DESCRIPTION'])



