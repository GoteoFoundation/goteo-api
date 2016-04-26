# -*- coding: utf-8 -*-

#from flask.ext.sqlalchemy import Pagination
from sqlalchemy import Integer, String, Text, Date, Boolean

from .. import db


class Blog(db.Model):
    __tablename__ = 'blog'

    id = db.Column('id', Integer, primary_key=True)
    type = db.Column('type', String(10))
    user_id = db.Column('owner', String(50), db.ForeignKey('user.id'))
    active = db.Column('active', Boolean)

    def __repr__(self):
        return '<Blog(%d) %s %s>' % (self.id, self.type, self.user_id)


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column('id', Integer, primary_key=True)
    blog_id = db.Column('blog', Integer, db.ForeignKey('blog.id'))
    title = db.Column('title', Text)
    date_publish = db.Column('date', Date)
    user_id = db.Column('author', String(50), db.ForeignKey('user.id'))
    publish = db.Column('publish', Integer)

    def __repr__(self):
        return '<Post(%d) %s: %s>' % (self.id, self.blog_id, self.title[:50])
