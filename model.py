# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
#from flask.ext.sqlalchemy import Pagination
from sqlalchemy import Integer, String, Text
from config import config

# DB class
#app = Flask(__name__)
app = Flask(__name__, static_url_path="")
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URI
app.config['SQLALCHEMY_ECHO'] = True

#
# Read debug status from config
if hasattr(config, 'debug'):
    app.debug = bool(config.debug)
    app.config['DEBUG'] = bool(config.debug)

#app.config['SQLALCHEMY_POOL_TIMEOUT'] = 5
#app.config['SQLALCHEMY_POOL_SIZE'] = 30
db = SQLAlchemy(app)
# app.config.from_pyfile(config)


# DB classes
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column('id', String(50), primary_key=True)
    name = db.Column('name', String(100))
    # email = db.Column('email', String(255))

    def __repr__(self):
        return '<User %s: %s>' % (self.name, self.email)


class Invest(db.Model):
    __tablename__ = 'invest'

    METHOD_PAYPAL = 'paypal'
    METHOD_TPV = 'tpv'
    METHOD_CASH = 'cash'
    METHOD_DROP = 'drop'

    id = db.Column('id', Integer, primary_key=True)
    user = db.Column('user', String(50))
    project = db.Column('project', String(50), db.ForeignKey('project.id'))
    status = db.Column('status', Integer)
    amount = db.Column('amount', Integer)
    method = db.Column('method', String(20))

    def __repr__(self):
        return '<Invest %d: %s (%d EUR)>' % (self.id, self.project, self.amount)


class Project(db.Model):
    __tablename__ = 'project'

    id = db.Column('id', String(50), primary_key=True)
    name = db.Column('name', Text)
    category = db.Column('category', String(50))
    minimum = db.Column('mincost', Integer)
    optimum = db.Column('maxcost', Integer)
    #subtitle = db.Column('subtitle', String(255))
    status = db.Column('status', Integer)
    #created = db.Column('created', Date)
    #updated = db.Column('updated', Date)
    #published = db.Column('published', Date)
    # total_funding
    # active_date
    # rewards
    # platform
    #aportes = db.relationship('Invest', backref='project')

    def __repr__(self):
        return '<Project %s: %s>' % (self.id, self.name)


class Call(db.Model):
    __tablename__ = 'call'

    id = db.Column('id', String(50), primary_key=True)
    name = db.Column('name', Text)
    amount = db.Column('amount', Integer)

    def __repr__(self):
        return '<Call %s: %s>' % (self.id, self.name)


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column('id', Integer, primary_key=True)
    name = db.Column('name', Text)

    def __repr__(self):
        return '<Category %s>' % (self.name)
