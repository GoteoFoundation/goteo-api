# -*- coding: utf-8 -*-

#from flask.ext.sqlalchemy import Pagination
from sqlalchemy import func, Integer, String, Text, Date, DateTime, Float
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from api.helpers import image_url, utc_from_local
from sqlalchemy import asc
from api import db



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

