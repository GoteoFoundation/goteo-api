# -*- coding: utf-8 -*-

from sqlalchemy import func, Integer, String, Text, Date, DateTime
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from api.helpers import image_url, utc_from_local
from sqlalchemy import asc, or_, distinct

from api.helpers import svg_image_url
from api import db

from api.models.location import Location, LocationItem
from api.models.reward import Reward
from api.models.project import Project,ProjectCategory


# License stuff
class License(db.Model):
    __tablename__ = 'license'

    id = db.Column('id', String(50), primary_key=True)
    name = db.Column('name', String(100))
    description = db.Column('description', Text)
    url = db.Column('url', String(255))
    order = db.Column('order', Integer)

    def __repr__(self):
        return '<License %s: %r>' % (self.id, self.name)

    @hybrid_property
    def svg_url(self):
    	return svg_image_url(self.id + '.svg')

    @hybrid_property
    def joins(self):
        return []

    #Filters for table license
    @hybrid_property
    def filters(self):
        return []

    # Getting filters for this model
    @hybrid_method
    def get_filters(self, **kwargs):
        filters = self.filters
        # Join project table if filters
        for i in ('node', 'from_date', 'to_date', 'category', 'location'):
            if i in kwargs and kwargs[i] is not None:
                filters.append(Project.status.in_([Project.STATUS_IN_CAMPAIGN,
                                                   Project.STATUS_FUNDED,
                                                   Project.STATUS_FULFILLED]))
        # Filters by goteo node
        if 'node' in kwargs and kwargs['node'] is not None:
            filters.append(Project.node == kwargs['node'])
        # Filters by "from date"
        # counting license created after this date
        if 'from_date' in kwargs and kwargs['from_date'] is not None:
            filters.append(Project.date_published >= kwargs['from_date'])
        # Filters by "to date"
        # counting license created before this date
        if 'to_date' in kwargs and kwargs['to_date'] is not None:
            filters.append(Project.date_published <= kwargs['to_date'])
        # Filters by "project"
        # counting attached (invested or collaborated) to some project(s)
        if 'project' in kwargs and kwargs['project'] is not None:
            subquery = db.session.query(Reward.license).filter(Reward.project.in_(kwargs['project']))
            filters.append(License.id.in_(subquery))
        # filter by license interests
        if 'category' in kwargs and kwargs['category'] is not None:
            filters.append(ProjectCategory.category == kwargs['category'])
        #Filter by location
        if 'location' in kwargs and kwargs['location'] is not None:
            locations_ids = Location.location_ids(**kwargs['location'])
            filters.append(LocationItem.type == 'project')
            filters.append(LocationItem.locable == True)
            filters.append(LocationItem.id.in_(locations_ids))

            pass
        return filters

    # Getting joins for this models
    @hybrid_method
    def get_joins(self, **kwargs):
        joins = self.joins
        for i in ('node', 'from_date', 'to_date', 'category', 'location'):
            if i in kwargs and kwargs[i] is not None:
                joins.append((Reward, Reward.license==License.id))
                joins.append((Project, Project.id==Reward.project))
        if 'category' in kwargs and kwargs['category'] is not None:
             joins.append((ProjectCategory, ProjectCategory.project==Reward.project))
        if 'location' in kwargs and kwargs['location'] is not None:
             joins.append((LocationItem, LocationItem.item==Reward.project))
        return joins

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
            joins = list(self.get_joins(**kwargs))
            return self.query.filter(*filters).distinct().join(*joins).order_by(asc(License.order)).all()
            # return self.query.filter(*filters).order_by(asc(License.order)).all()
        except NoResultFound:
            return []

    @hybrid_method
    def total(self, **kwargs):
        """Returns the total number of valid license"""
        try:
            filters = list(self.get_filters(**kwargs))
            joins = list(self.get_joins(**kwargs))
            # count = db.session.query(func.count(distinct(License.id))).filter(*filters).scalar()
            count = db.session.query(func.count(distinct(License.id))).filter(*filters).join(*joins).scalar()
            if count is None:
                count = 0
            return count
        except MultipleResultsFound:
            return 0

