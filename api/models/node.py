# -*- coding: utf-8 -*-

#from flask.ext.sqlalchemy import Pagination
from sqlalchemy import Integer, String

from .. import db

class Node(db.Model):
    __tablename__ = 'node'

    id = db.Column('id', String(50), primary_key=True)
    name = db.Column('name', String(256))
    active = db.Column('active', Integer)

    def __repr__(self):
        return '<Node(%d): %s>' % (self.id, self.name)


