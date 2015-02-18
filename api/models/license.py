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

# DEBUG
if config.debug:
    db.session.query = debug_time(db.session.query)

# License stuff
class License(db.Model):
    __tablename__ = 'license'

    id = db.Column('id', String(50), primary_key=True)
    name = db.Column('name', String(100))
    description = db.Column('description', Text)
    order = db.Column('order', Integer)

    def __repr__(self):
        return '<License %s: %r>' % (self.id, self.name)

    @hybrid_property
    def svg_url(self):
    	return svg_image_url(self.id + '.svg')

    #Filters for table license
    @hybrid_property
    def filters(self):
        return []

    # Getting filters for this model
    @hybrid_method
    def get_filters(self, **kwargs):
        filters = self.filters
        # Filters by goteo node
        if 'node' in kwargs and kwargs['node'] is not None:
            # filters.append(License.node.in_(kwargs['node']))
            pass
        # Filters by "from date"
        # counting license created after this date
        if 'from_date' in kwargs and kwargs['from_date'] is not None:
            # filters.append(License.created >= kwargs['from_date'])
            pass
        # Filters by "to date"
        # counting license created before this date
        if 'to_date' in kwargs and kwargs['to_date'] is not None:
            # filters.append(License.created <= kwargs['to_date'])
            pass
        # Filters by "project"
        # counting attached (invested or collaborated) to some project(s)
        if 'project' in kwargs and kwargs['project'] is not None:
        	pass
        # filter by license interests
        if 'category' in kwargs and kwargs['category'] is not None:
            pass
        #Filter by location
        if 'location' in kwargs and kwargs['location'] is not None:
            pass
        #TODO: more filters, like creators, invested, etc
        return filters

    @hybrid_method
    def get(self, id):
        """Get a valid license form id"""
        try:
            filters = list(self.filters)
            filters.append(License.id == id)
            return self.query.filter(*filters).one()
        except NoResultFound:
            return None

    @hybrid_method
    def list(self, **kwargs):
        """Get a list of valid license"""
        try:
            filters = list(self.get_filters(**kwargs))
            # joins = list(self.get_joins(**kwargs))
            # outerjoins = list(self.get_outerjoins(**kwargs))
            # return self.query.filter(*filters).join(*joins).outerjoin(*outerjoins).order_by(asc(License.id)).offset(page * limit).limit(limit)
            return self.query.filter(*filters).order_by(asc(License.order)).all()
        except NoResultFound:
            return []

    @hybrid_method
    def total(self, **kwargs):
        """Returns the total number of valid license"""
        try:
            filters = list(self.get_filters(**kwargs))
            # joins = list(self.get_joins(**kwargs))
            # outerjoins = list(self.get_outerjoins(**kwargs))
            # count = db.session.query(func.count(distinct(License.id))).filter(*filters).join(*joins).outerjoin(*outerjoins).scalar()
            count = db.session.query(func.count(distinct(License.id))).filter(*filters).scalar()
            if count is None:
                count = 0
            return count
        except MultipleResultsFound:
            return 0