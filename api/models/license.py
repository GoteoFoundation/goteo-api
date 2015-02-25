# -*- coding: utf-8 -*-

from sqlalchemy import func, Integer, String, Text, Date, DateTime
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from api.helpers import image_url, utc_from_local
from sqlalchemy import asc, or_, distinct

from api.helpers import svg_image_url
from api import db

# License stuff
class License(db.Model):
    __tablename__ = 'license'

    id = db.Column('id', String(50), primary_key=True)
    license = db.Column('name', String(100))
    description = db.Column('description', Text)
    url = db.Column('url', String(255))
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
        from .location import Location, LocationItem
        from .reward import Reward
        from .project import Project, ProjectCategory

        filters = self.filters
        # Join project table if filters
        for i in ('node', 'from_date', 'to_date', 'project', 'category', 'location'):
            if i in kwargs and kwargs[i] is not None:
                filters.append(Reward.license == self.id)
                filters.append(Project.id == Reward.project)
                filters.append(Project.status.in_(Project.SUCCESSFUL_PROJECTS))
        # Filters by goteo node
        if 'node' in kwargs and kwargs['node'] is not None:
            filters.append(Project.node.in_(kwargs['node']))
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
            filters.append(Project.id.in_(kwargs['project']))
        # filter by license interests
        if 'category' in kwargs and kwargs['category'] is not None:
            filters.append(ProjectCategory.project == Reward.project)
            filters.append(ProjectCategory.category.in_(kwargs['category']))
        #Filter by location
        if 'location' in kwargs and kwargs['location'] is not None:
            locations_ids = Location.location_ids(**kwargs['location'])
            filters.append(LocationItem.type == 'project')
            filters.append(LocationItem.item == Reward.project)
            filters.append(LocationItem.locable == True)
            filters.append(LocationItem.id.in_(locations_ids))

            pass
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
            return self.query.filter(*filters).order_by(asc(License.order)).all()
        except NoResultFound:
            return []

    @hybrid_method
    def total(self, **kwargs):
        """Returns the total number of valid license"""
        try:
            filters = list(self.get_filters(**kwargs))
            count = db.session.query(func.count(distinct(License.id))).filter(*filters).scalar()
            if count is None:
                count = 0
            return count
        except MultipleResultsFound:
            return 0

