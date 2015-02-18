# -*- coding: utf-8 -*-

from sqlalchemy import func, Integer, String, Text, Date, DateTime
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from api.helpers import image_url, utc_from_local
from sqlalchemy import asc, or_, distinct

from api.helpers import debug_time, svg_image_url
from config import config
from api import db

from api.models.location import Location, LocationItem


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column('id', Integer, primary_key=True)
    name = db.Column('name', Text)
    description = db.Column('description', Text)
    order = db.Column('order', Integer)

    def __repr__(self):
        return '<Category %s>' % (self.name)

    #Filters for table category
    @hybrid_property
    def filters(self):
        return [Category.name != '']

    # Getting filters for this model
    @hybrid_method
    def get_filters(self, **kwargs):
        filters = self.filters
        # Filters by goteo node
        if 'node' in kwargs and kwargs['node'] is not None:
            # filters.append(Category.node.in_(kwargs['node']))
            pass
        # Filters by "from date"
        # counting category created after this date
        if 'from_date' in kwargs and kwargs['from_date'] is not None:
            # filters.append(Category.created >= kwargs['from_date'])
            pass
        # Filters by "to date"
        # counting category created before this date
        if 'to_date' in kwargs and kwargs['to_date'] is not None:
            # filters.append(Category.created <= kwargs['to_date'])
            pass
        # Filters by "project"
        # counting attached (invested or collaborated) to some project(s)
        if 'project' in kwargs and kwargs['project'] is not None:
        	pass
        # filter by category interests
        if 'category' in kwargs and kwargs['category'] is not None:
            pass
        #Filter by location
        if 'location' in kwargs and kwargs['location'] is not None:
            pass
        #TODO: more filters, like creators, invested, etc
        return filters

    @hybrid_method
    def get(self, id):
        """Get a valid category form id"""
        try:
            filters = list(self.filters)
            filters.append(Category.id == id)
            return self.query.filter(*filters).one()
        except NoResultFound:
            return None

    @hybrid_method
    def list(self, **kwargs):
        """Get a list of valid category"""
        try:
            filters = list(self.get_filters(**kwargs))
            return self.query.filter(*filters).order_by(asc(Category.order)).all()
        except NoResultFound:
            return []

    @hybrid_method
    def total(self, **kwargs):
        """Returns the total number of valid category"""
        try:
            filters = list(self.get_filters(**kwargs))
            count = db.session.query(func.count(distinct(Category.id))).filter(*filters).scalar()
            if count is None:
                count = 0
            return count
        except MultipleResultsFound:
            return 0