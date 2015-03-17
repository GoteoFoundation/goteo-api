# -*- coding: utf-8 -*-

#from flask.ext.sqlalchemy import Pagination
from sqlalchemy import Integer, String, Text

from .. import db


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

