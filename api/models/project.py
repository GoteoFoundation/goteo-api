# -*- coding: utf-8 -*-

#from flask.ext.sqlalchemy import Pagination
from sqlalchemy import func, Integer, String, Text, Date, DateTime, Float
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from api.helpers import image_url, utc_from_local
from sqlalchemy import asc, distinct
from api import db

class Project(db.Model):
    __tablename__ = 'project'

    #PROJECT STATUS IDs
    STATUS_REJECTED    = 0
    STATUS_EDITING     = 1
    STATUS_REVIEWING   = 2
    STATUS_IN_CAMPAIGN = 3
    STATUS_FUNDED      = 4
    STATUS_FULFILLED   = 5 # 'Caso de exito'
    STATUS_UNFUNDED    = 6 # proyecto fallido

    PUBLISHED_PROJECTS = [STATUS_IN_CAMPAIGN, STATUS_FUNDED, STATUS_FULFILLED, STATUS_UNFUNDED]
    SUCCESSFUL_PROJECTS = [STATUS_IN_CAMPAIGN, STATUS_FUNDED, STATUS_FULFILLED]

    id = db.Column('id', String(50), primary_key=True)
    owner = db.Column('owner', String(50), db.ForeignKey('user.id'))
    name = db.Column('name', Text)
    minimum = db.Column('mincost', Integer)
    optimum = db.Column('maxcost', Integer)
    #subtitle = db.Column('subtitle', String(255))
    status = db.Column('status', Integer)
    #created = db.Column('created', Date)
    date_passed = db.Column('passed', Date)
    date_updated = db.Column('updated', Date)
    date_published = db.Column('published', Date)
    date_closed = db.Column('closed', Date)
    node = db.Column('node', String(50), db.ForeignKey('node.id'))
    # total_funding
    # active_date
    # rewards
    # platform
    #aportes = db.relationship('Invest', backref='project')

    def __repr__(self):
        return '<Project %s: %s>' % (self.id, self.name)

    #Filters for this table
    @hybrid_property
    def filters(self):
        return [self.status.in_(self.PUBLISHED_PROJECTS)]

    # Getting filters for this model
    @hybrid_method
    def get_filters(self, **kwargs):
        from .reward import Reward
        from .location import Location, LocationItem
        filters = self.filters
        # # Join project table if filters
        for i in ('license', 'license_type'):
            if i in kwargs and kwargs[i] is not None:
                filters.append(self.id == Reward.project)
        if 'license_type' in kwargs and kwargs['license_type'] is not None:
            filters.append(Reward.type == kwargs['license_type'])
        if 'license' in kwargs and kwargs['license'] is not None:
            filters.append(Reward.license.in_(kwargs['license']))
        if 'from_date' in kwargs and kwargs['from_date'] is not None:
            filters.append(self.date_published >= kwargs['from_date'])
        if 'to_date' in kwargs and kwargs['to_date'] is not None:
            filters.append(self.date_published <= kwargs['to_date'])
        if 'project' in kwargs and kwargs['project'] is not None:
            filters.append(self.id.in_(kwargs['project']))
        if 'node' in kwargs and kwargs['node'] is not None:
            filters.append(self.node.in_(kwargs['node']))
        if 'category' in kwargs and kwargs['category'] is not None:
            filters.append(self.id == ProjectCategory.project)
            filters.append(ProjectCategory.category.in_(kwargs['category']))
        if 'location' in kwargs and kwargs['location'] is not None:
            subquery = Location.location_subquery(**kwargs['location'])
            filters.append(LocationItem.type == 'project')
            filters.append(LocationItem.item == self.id)
            filters.append(LocationItem.locable == True)
            filters.append(LocationItem.id.in_(subquery))

        return filters

    @hybrid_method
    def total(self, **kwargs):
        """Total number of projects"""
        try:
            filters = list(self.get_filters(**kwargs))
            total = db.session.query(func.count(distinct(Project.id))).filter(*filters).scalar()
            if total is None:
                total = 0
            return total
        except MultipleResultsFound:
            return 0




class ProjectCategory(db.Model):
    __tablename__ = 'project_category'

    project = db.Column('project', String(50), db.ForeignKey('project.id'), primary_key=True)
    category = db.Column('category', Integer, db.ForeignKey('category.id'), primary_key=True)

    def __repr__(self):
        return '<Category %s>' % (self.name)

