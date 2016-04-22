# -*- coding: utf-8 -*-

from sqlalchemy import func, Integer, String, Text
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.orm import aliased
from sqlalchemy import asc,desc,and_, distinct

from ..helpers import get_lang, objectview
from ..cacher import cacher

from .icon import Icon, IconLang
from ..projects.models import Project, ProjectCategory

from .. import db

# Reward stuff
class Reward(db.Model):
    __tablename__ = 'reward'

    id = db.Column('id', Integer, primary_key=True)
    project_id = db.Column('project', String(50), db.ForeignKey('project.id'))
    reward = db.Column('reward', String(50))
    description = db.Column('description', Text)
    type = db.Column('type', String(50))
    amount = db.Column('amount', Integer)
    icon = db.Column('icon', String(50), db.ForeignKey('icon.id'))
    license = db.Column('license', String(50), db.ForeignKey('license.id'))
    order = db.Column('order', Integer)

    def __repr__(self):
        return '<Reward(%d) %s: %s>' % (self.id, self.project_id[:10], self.title[:50])

    #Filters for this table
    @hybrid_property
    def filters(self):
        return []

    # Getting filters for this model
    @hybrid_method
    def get_filters(self, **kwargs):
        from ..location.models import ProjectLocation

        filters = self.filters
        # Join project table if filters
        for i in ('node', 'from_date', 'to_date', 'project', 'category', 'location'):
            if i in kwargs and kwargs[i] is not None:
                filters.append(Project.id == self.project_id)
                filters.append(Project.status.in_(Project.PUBLISHED_PROJECTS))
        if 'license_type' in kwargs and kwargs['license_type'] is not None:
            filters.append(self.type == kwargs['license_type'])
        if 'license' in kwargs and kwargs['license'] is not None:
            filters.append(self.license.in_(kwargs['license']))
        if 'from_date' in kwargs and kwargs['from_date'] is not None:
            filters.append(Project.published >= kwargs['from_date'])
        if 'to_date' in kwargs and kwargs['to_date'] is not None:
            filters.append(Project.published <= kwargs['to_date'])
        if 'project' in kwargs and kwargs['project'] is not None:
            filters.append(self.project_id.in_(kwargs['project']))
        if 'node' in kwargs and kwargs['node'] is not None:
            filters.append(Project.node.in_(kwargs['node']))
        if 'category' in kwargs and kwargs['category'] is not None:
            filters.append(Project.id == ProjectCategory.project_id)
            filters.append(ProjectCategory.category_id.in_(kwargs['category']))
        if 'location' in kwargs and kwargs['location'] is not None:
            subquery = ProjectLocation.location_subquery(**kwargs['location'])
            filters.append(ProjectLocation.id == self.project_id)
            filters.append(ProjectLocation.id.in_(subquery))

        return filters

    @hybrid_method
    @cacher
    def list(self, **kwargs):
        """Get a list of valid rewards"""
        try:
            limit = kwargs['limit'] if 'limit' in kwargs else 10
            page = kwargs['page'] if 'page' in kwargs else 0
            filters = self.get_filters(**kwargs)
            return self.query.distinct().filter(*filters).order_by(asc(self.order), asc(self.amount)).offset(page * limit).limit(limit).all()
        except NoResultFound:
            return []

    @hybrid_method
    @cacher
    def list_by_project(self, project_id):
        """Get a list of valid rewards for project"""
        try:
            return self.query.distinct().filter(self.project_id==project_id).order_by(asc(self.order), asc(self.amount)).all()
        except NoResultFound:
            return []

    @hybrid_method
    @cacher
    def total(self, **kwargs):
        """Total number of rewards"""
        try:
            filters = list(self.get_filters(**kwargs))
            total = db.session.query(func.count(distinct(self.id))).filter(*filters).scalar()
            if total is None:
                total = 0
            return total
        except MultipleResultsFound:
            return 0

    @hybrid_method
    @cacher
    def favorite_reward(self, **kwargs):
        """Reward type used in successful projects"""

        filters = list(self.get_filters(**kwargs))

        cols = [self.icon, Icon.svg_url.label('svg-url'), Icon.name, Icon.description, func.count(self.project_id).label('total')]
        injoins = [(Project, and_(Project.id == self.project_id, Project.status.in_(Project.SUCCESSFUL_PROJECTS))),
                   (Icon, Icon.id == self.icon)]

        if 'lang' in kwargs and kwargs['lang'] is not None:
            # In case of requiring languages, a LEFT JOIN must be generated
            joins = []
            for l in kwargs['lang']:
                alias = aliased(IconLang)
                cols.append(alias.name.label('name_' + l))
                cols.append(alias.description.label('description_' + l))
                joins.append((alias, and_(alias.id == Icon.id, alias.lang == l)))
            query = db.session.query(*cols).join(*injoins).outerjoin(*joins)
        else:
            query = db.session.query(*cols).join(*injoins)

        ret = []
        for u in query.filter(*filters).group_by(self.icon).order_by(desc('total')):
            u = u._asdict()
            if 'lang' in kwargs and kwargs['lang'] is not None:
                u['name'] = get_lang(u, 'name', kwargs['lang'])
                u['description'] = get_lang(u, 'description', kwargs['lang'])
            ret.append(objectview(u))
        if ret is None:
            ret = []
        return ret
