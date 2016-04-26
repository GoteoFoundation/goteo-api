# -*- coding: utf-8 -*-

from sqlalchemy import func, Integer, String, Text
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy import asc, distinct

from ..helpers import svg_image_url
from ..base_resources import AbstractLang
from ..cacher import cacher

from .. import db


# License stuff
class LicenseLang(AbstractLang, db.Model):
    __tablename__ = 'license_lang'

    id = db.Column('id', String(50), db.ForeignKey('license.id'), primary_key=True)
    lang = db.Column('lang', String(2), primary_key=True)
    name = db.Column('name', String(100))
    description = db.Column('description', Text)
    url = db.Column('url', String(255))
    pending = db.Column('pending', Integer)

    def __repr__(self):
        return '<LicenseLang %s(%s): %r>' % (self.id, self.lang, self.name)

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

    #Filters for table license
    @hybrid_property
    def filters(self):
        return []

    # Getting filters for this model
    @hybrid_method
    def get_filters(self, **kwargs):

        from ..models.reward import Reward
        from ..projects.models import Project, ProjectCategory
        from ..location.models import ProjectLocation

        filters = self.filters
        # Join project table if filters
        for i in ('node', 'from_date', 'to_date', 'project', 'category', 'location'):
            if i in kwargs and kwargs[i] is not None:
                filters.append(Reward.license_id == self.id)
                filters.append(Project.id == Reward.project_id)
                filters.append(Project.status.in_(Project.PUBLISHED_PROJECTS))
        # Filters by goteo node
        if 'node' in kwargs and kwargs['node'] is not None:
            filters.append(Project.node_id.in_(kwargs['node']))
        # Filters by "from date"
        # counting license created after this date
        if 'from_date' in kwargs and kwargs['from_date'] is not None:
            filters.append(Project.published >= kwargs['from_date'])
        # Filters by "to date"
        # counting license created before this date
        if 'to_date' in kwargs and kwargs['to_date'] is not None:
            filters.append(Project.published <= kwargs['to_date'])
        # Filters by "project"
        # counting attached (invested or collaborated) to some project(s)
        if 'project' in kwargs and kwargs['project'] is not None:
            filters.append(Project.id.in_(kwargs['project']))
        # filter by license interests
        if 'category' in kwargs and kwargs['category'] is not None:
            filters.append(ProjectCategory.project_id == Reward.project_id)
            filters.append(ProjectCategory.category_id.in_(kwargs['category']))
        #Filter by location
        if 'location' in kwargs and kwargs['location'] is not None:
            filters.append(ProjectLocation.id == Reward.project_id)
            subquery = ProjectLocation.location_subquery(**kwargs['location'])
            filters.append(ProjectLocation.id.in_(subquery))

        return filters

    @hybrid_method
    @cacher
    def get(self, id):
        """Get a valid license form id"""
        try:
            filters = list(self.filters)
            filters.append(License.id == id)
            return self.query.filter(*filters).one()
        except NoResultFound:
            return None

    @hybrid_method
    @cacher
    def list(self, **kwargs):
        """Get a list of valid license"""
        try:
            filters = list(self.get_filters(**kwargs))

            # In case of requiring languages, a LEFT JOIN must be generated
            if 'lang' in kwargs and kwargs['lang'] is not None:
                ret = []
                for u in LicenseLang.get_query(kwargs['lang']) \
                                 .filter(*filters).order_by(asc(self.order)):
                    ret.append(LicenseLang.get_translated_object(u._asdict(), kwargs['lang']))
                return ret
            # No langs, normal query
            return self.query.distinct().filter(*filters) \
                                        .order_by(asc(self.order)).all()
        except NoResultFound:
            return []

    @hybrid_method
    @cacher
    def total(self, **kwargs):
        """Returns the total number of valid license"""
        try:
            filters = list(self.get_filters(**kwargs))
            count = db.session.query(func.count(distinct(self.id))).filter(*filters).scalar()
            if count is None:
                count = 0
            return count
        except MultipleResultsFound:
            return 0

