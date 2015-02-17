# -*- coding: utf-8 -*-

#from flask.ext.sqlalchemy import Pagination
from sqlalchemy import func, Integer, String, Text, Date, DateTime, Float
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from api.helpers import image_url, utc_from_local
from sqlalchemy import asc
from api import db


class Project(db.Model):
    __tablename__ = 'project'

    #PROJECT STATUS IDs
    STATUS_REJECTED    = 0
    STATUS_EDITING     = 1
    STATUS_REVIEWING   = 2
    STATUS_IN_CAMPAIGN = 3
    STATUS_FUNDED      = 4
    STATUS_FULLFILED   = 5 # 'Caso de exito'
    STATUS_UNFUNDED    = 6 # proyecto fallido

    id = db.Column('id', String(50), primary_key=True)
    owner = db.Column('owner', String(50), db.ForeignKey('user.id'))
    name = db.Column('name', Text)
    category = db.Column('category', String(50), db.ForeignKey('category.id'))
    minimum = db.Column('mincost', Integer)
    optimum = db.Column('maxcost', Integer)
    #subtitle = db.Column('subtitle', String(255))
    status = db.Column('status', Integer)
    #created = db.Column('created', Date)
    date_passed = db.Column('passed', Date)
    date_updated = db.Column('updated', Date)
    date_published = db.Column('published', Date)
    date_closed = db.Column('closed', Date)
    node = db.Column('node', String(50), db.ForeignKey('node.id'))
    # total_funding
    # active_date
    # rewards
    # platform
    #aportes = db.relationship('Invest', backref='project')

    def __repr__(self):
        return '<Project %s: %s>' % (self.id, self.name)


class Node(db.Model):
    __tablename__ = 'node'

    id = db.Column('id', String(50), primary_key=True)
    name = db.Column('name', String(256))
    active = db.Column('active', Integer)

    def __repr__(self):
        return '<Node(%d): %s>' % (self.id, self.name)


class Call(db.Model):
    __tablename__ = 'call'

    #CALL STATUS IDs
    STATUS_CANCELED   = 0
    STATUS_EDITING    = 1
    STATUS_REVIEWING  = 2
    STATUS_APPLYING   = 3
    STATUS_PUBLISHING = 4
    STATUS_COMPLETED  = 5
    STATUS_EXPIRED    = 6

    id = db.Column('id', String(50), primary_key=True)
    name = db.Column('name', Text)
    amount = db.Column('amount', Integer)
    owner = db.Column('owner', String(50))
    status = db.Column('status', Integer)
    date_published = db.Column('published', Date)

    def __repr__(self):
        return '<Call %s: %s>' % (self.id, self.name)


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column('id', Integer, primary_key=True)
    name = db.Column('name', Text)

    def __repr__(self):
        return '<Category %s>' % (self.name)


class ProjectCategory(db.Model):
    __tablename__ = 'project_category'

    project = db.Column('project', String(50), db.ForeignKey('project.id'), primary_key=True)
    category = db.Column('category', Integer, db.ForeignKey('category.id'), primary_key=True)

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
    blog = db.Column('blog', Integer, db.ForeignKey('blog.id'))
    title = db.Column('title', Text)
    date_publish = db.Column('date', Date)
    author = db.Column('author', String(50), db.ForeignKey('user.id'))
    publish = db.Column('publish', Integer)

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


class Message(db.Model):
    __tablename__ = 'message'

    id = db.Column('id', Integer, primary_key=True)
    project = db.Column('project', String(50), db.ForeignKey('project.id'))
    user = db.Column('user', String(50), db.ForeignKey('user.id'))
    thread = db.Column('thread', Integer)
    blocked = db.Column('blocked', Integer)
    date = db.Column('date', DateTime)
    # message = db.Column('message', Text)

    def __repr__(self):
        return '<Message(%d) from %s to project %s>' % (self.id, self.user, self.project)


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

