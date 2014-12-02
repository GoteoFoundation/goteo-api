# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
#from flask.ext.sqlalchemy import Pagination
from sqlalchemy import Integer, String, Text, Date, Boolean
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
    active = db.Column('active', Integer)
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
    user = db.Column('user', String(50), db.ForeignKey('user.id'))
    project = db.Column('project', String(50), db.ForeignKey('project.id'))
    status = db.Column('status', Integer)
    amount = db.Column('amount', Integer)
    method = db.Column('method', String(20))
    date_invested = db.Column('invested', Date)
    date_charged = db.Column('charged', Date)
    resign = db.Column('resign', Integer)

    def __repr__(self):
        return '<Invest %d: %s (%d EUR)>' % (self.id, self.project, self.amount)


class Project(db.Model):
    __tablename__ = 'project'

    id = db.Column('id', String(50), primary_key=True)
    owner = db.Column('owner', String(50), db.ForeignKey('user.id'))
    name = db.Column('name', Text)
    category = db.Column('category', String(50))
    minimum = db.Column('mincost', Integer)
    optimum = db.Column('maxcost', Integer)
    #subtitle = db.Column('subtitle', String(255))
    status = db.Column('status', Integer)
    #created = db.Column('created', Date)
    date_passed = db.Column('passed', Date)
    date_updated = db.Column('updated', Date)
    date_published = db.Column('published', Date)
    date_closed = db.Column('closed', Date)
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


class Blog(db.Model):
    __tablename__ = 'blog'

    id = db.Column('id', Integer, primary_key=True)
    type = db.Column('type', String(10))
    owner = db.Column('owner', String(50))
    active = db.Column('active', Integer)

    def __repr__(self):
        return '<Blog(%d) %s %s>' % (self.id, self.type, self.owner)


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column('id', Integer, primary_key=True)
    blog = db.Column('blog', Integer), db.ForeignKey('blog.id')
    title = db.Column('title', Text)
    date_publish = db.Column('publish', Boolean)
    author = db.Column('author', String(50), db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post(%d) %s: %s>' % (self.id, self.blog, self.title[:50])


class Reward(db.Model):
    __tablename__ = 'reward'

    id = db.Column('id', Integer, primary_key=True)
    project = db.Column('project', String(50), db.ForeignKey('project.id'))
    reward = db.Column('reward', Text)
    type = db.Column('type', String(50))
    amount = db.Column('amount', Integer)
    icon = db.Column('icon', String(50))

    def __repr__(self):
        return '<Reward(%d) %s: %s>' % (self.id, self.project[:10], self.title[:50])


# TODO: backrefs
class InvestReward(db.Model):
    __tablename__ = 'invest_reward'

    invest = db.Column('invest', Integer, db.ForeignKey('invest.id'), primary_key=True)
    reward = db.Column('reward', Integer, db.ForeignKey('reward.id'), primary_key=True)

    def __repr__(self):
        return '<Invest(%d) - Reward(%d)>' % (self.invest, self.reward)


class Message(db.Model):
    __tablename__ = 'message'

    id = db.Column('id', Integer, primary_key=True)
    project = db.Column('project', String(50), db.ForeignKey('project.id'))
    user = db.Column('user', String(50), db.ForeignKey('user.id'))
    thread = db.Column('thread', Integer)
    blocked = db.Column('blocked', Integer)
    # message = db.Column('message', Text)

    def __repr__(self):
        return '<Message(%d) from %s to project %s>' % (self.id, self.user, self.project)


class UserInterest(db.Model):
    __tablename__ = 'user_interest'

    user = db.Column('user', String(50), db.ForeignKey('user.id'), primary_key=True)
    interest = db.Column('interest', Integer, db.ForeignKey('category.id'), primary_key=True)

    def __repr__(self):
        return '<UserInterest from %s to project %s>' % (self.user, self.project)


class Cost(db.Model):
    __tablename__ = 'cost'

    id = db.Column('id', Integer, primary_key=True)
    cost = db.Column('cost', Text)
    description = db.Column('description', Text)
    type = db.Column('type', String(50))
    project = db.Column('project', String(50))
    amount = db.Column('amount', Integer)
    required = db.Column('required', Integer)

    def __repr__(self):
        return '<Cost(%d) %s of project %s>' % (self.id, self.cost[:50], self.project)
