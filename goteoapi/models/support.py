# -*- coding: utf-8 -*-

#from flask.ext.sqlalchemy import Pagination
from sqlalchemy import Integer, String, Text
from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import asc

from ..cacher import cacher

from .. import db


class Support(db.Model):
    __tablename__ = 'support'

    id = db.Column('id', Integer, primary_key=True)
    support = db.Column('support', Text)
    description = db.Column('description', Text)
    type = db.Column('type', String(50))
    project = db.Column('project', String(50), db.ForeignKey('project.id'))
    thread = db.Column('thread', Integer)

    def __repr__(self):
        return '<Support(%d) %s of project %s>' % (self.id, self.support, self.project)


    @hybrid_method
    @cacher
    def list_by_project(self, project_id):
        """Get a list of valid supports (non-economic needs) for project"""
        try:
            return self.query.distinct().filter(self.project==project_id).order_by(asc(self.id)).all()
        except NoResultFound:
            return []
