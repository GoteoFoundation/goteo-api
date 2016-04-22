# -*- coding: utf-8 -*-

#from flask.ext.sqlalchemy import Pagination
from sqlalchemy import Integer, String, Text, Boolean, Date
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import asc

from ..helpers import utc_from_local
from ..cacher import cacher

from .. import db


class Cost(db.Model):
    __tablename__ = 'cost'

    id = db.Column('id', Integer, primary_key=True)
    cost = db.Column('cost', Text)
    description = db.Column('description', Text)
    type = db.Column('type', String(50))
    project_id = db.Column('project', String(50), db.ForeignKey('project.id'))
    amount = db.Column('amount', Integer)
    required = db.Column('required', Boolean)
    from_date = db.Column('from', Date)
    to_date = db.Column('until', Date)

    def __repr__(self):
        return '<Cost(%d) %s of project %s>' % (self.id, self.cost[:50], self.project_id)

    @hybrid_property
    def date_from(self):
        return utc_from_local(self.from_date)

    @hybrid_property
    def date_to(self):
        return utc_from_local(self.to_date)

    @hybrid_method
    @cacher
    def list_by_project(self, project_id):
        """Get a list of valid costs for project"""
        try:
            return self.query.distinct().filter(self.project_id==project_id).order_by(asc(self.from_date)).all()
        except NoResultFound:
            return []
