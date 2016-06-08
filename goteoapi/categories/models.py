# -*- coding: utf-8 -*-

from sqlalchemy import func, Integer, String, Text
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy import asc, distinct

from ..base_resources import AbstractLang
from ..cacher import cacher

from .. import db


class CategoryLang(AbstractLang, db.Model):
    __tablename__ = 'category_lang'

    id = db.Column('id', Integer,
                   db.ForeignKey('category.id'), primary_key=True)
    lang = db.Column('lang', String(2), primary_key=True)
    name = db.Column('name', Text)
    description = db.Column('description', Text)
    pending = db.Column('pending', Integer)

    def __repr__(self):
        return '<CategoryLang %s(%s): %r>' % (self.id, self.lang, self.name)


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column('id', Integer, primary_key=True)
    name = db.Column('name', Text)
    description = db.Column('description', Text)
    order = db.Column('order', Integer)

    def __repr__(self):
        return '<Category %s: %r>' % (self.id, self.name)

    # Filters for table category
    @hybrid_property
    def filters(self):
        return [self.name != '']

    # Getting filters for this model
    @hybrid_method
    def get_filters(self, **kwargs):

        from ..projects.models import Project, ProjectCategory
        from ..location.models import ProjectLocation

        filters = self.filters
        # Join project table if filters
        for i in ('node', 'from_date', 'to_date', 'project', 'location'):
            if i in kwargs and kwargs[i] is not None:
                filters.append(self.id == ProjectCategory.category_id)
                filters.append(Project.id == ProjectCategory.project_id)
                filters.append(Project.status.in_(Project.PUBLISHED_PROJECTS))

        # Filters by goteo node
        if 'node' in kwargs and kwargs['node'] is not None:
            filters.append(Project.node_id.in_(kwargs['node']))
        # Filters by "from date"
        # counting category created after this date
        if 'from_date' in kwargs and kwargs['from_date'] is not None:
            filters.append(Project.published >= kwargs['from_date'])
        # Filters by "to date"
        # counting category created before this date
        if 'to_date' in kwargs and kwargs['to_date'] is not None:
            filters.append(Project.published <= kwargs['to_date'])
        # Filters by "project"
        # counting attached (invested or collaborated) to some project(s)
        if 'project' in kwargs and kwargs['project'] is not None:
            filters.append(Project.id.in_(kwargs['project']))
        # filter by category interests
        if 'category' in kwargs and kwargs['category'] is not None:
            filters.append(self.id.in_(kwargs['category']))
        # Filter by location
        if 'location' in kwargs and kwargs['location'] is not None:
            filters.append(ProjectLocation.id == ProjectCategory.project_id)
            subquery = ProjectLocation.location_subquery(**kwargs['location'])
            filters.append(ProjectLocation.id.in_(subquery))

        return filters

    @hybrid_method
    @cacher
    def get(self, id):
        """Get a valid category from id"""
        try:
            filters = list(self.filters)
            filters.append(self.id == id)
            return self.query.filter(*filters).one()
        except NoResultFound:
            return None

    @hybrid_method
    @cacher
    def list(self, **kwargs):
        """Get a list of valid category"""
        try:
            filters = list(self.get_filters(**kwargs))
            # In case of requiring languages, a LEFT JOIN must be generated
            if 'lang' in kwargs and kwargs['lang'] is not None:
                ret = []
                for u in CategoryLang.get_query(kwargs['lang']) \
                                     .filter(*filters) \
                                     .order_by(asc(self.order)):
                    ret.append(CategoryLang.get_translated_object(
                        u._asdict(), kwargs['lang']))
                return ret
            # No langs, normal query
            return self.query.distinct().filter(*filters) \
                                        .order_by(asc(self.order)).all()

        except NoResultFound:
            return []

    @hybrid_method
    @cacher
    def total(self, **kwargs):
        """Returns the total number of valid category"""
        try:
            filters = list(self.get_filters(**kwargs))
            count = db.session.query(func.count(distinct(self.id))) \
                              .filter(*filters).scalar()
            if count is None:
                count = 0
            return count
        except MultipleResultsFound:
            return 0
