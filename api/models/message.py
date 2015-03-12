# -*- coding: utf-8 -*-

#from flask.ext.sqlalchemy import Pagination
from sqlalchemy import func, Integer, String, DateTime
from sqlalchemy.ext.hybrid import hybrid_method
from api import db
from .project import ProjectCategory
from .location import Location, LocationItem
from ..decorators import cacher

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

    # Getting filters for this model
    @hybrid_method
    def get_filters(self, **kwargs):
        filters = []
        if 'from_date' in kwargs and kwargs['from_date'] is not None:
            filters.append(self.date >= kwargs['from_date'])
        if 'to_date' in kwargs and kwargs['to_date'] is not None:
            filters.append(self.date <= kwargs['to_date'])
        if 'project' in kwargs and kwargs['project'] is not None:
            filters.append(self.project.in_(kwargs['project']))
        if 'node' in kwargs and kwargs['node'] is not None:
            from .user import User
            filters.append(self.user == User.id)
            filters.append(User.node.in_(kwargs['node']))
        if 'category' in kwargs and kwargs['category'] is not None:
            filters.append(self.project == ProjectCategory.project)
            filters.append(ProjectCategory.category.in_(kwargs['category']))
        if 'location' in kwargs and kwargs['location'] is not None:
            filters.append(self.user == LocationItem.item)
            filters.append(LocationItem.type == 'user')
            subquery = Location.location_subquery(**kwargs['location'])
            filters.append(LocationItem.id.in_(subquery))

        return filters
    @hybrid_method
    @cacher
    def collaborators_total(self, **kwargs):
        """Total number of collaborators"""
        filters = list(self.get_filters(**kwargs))
        res = db.session.query(func.count(func.distinct(Message.user))).filter(*filters).scalar()
        if res is None:
            res = 0
        return res
