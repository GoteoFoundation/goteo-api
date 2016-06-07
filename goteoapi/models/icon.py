# -*- coding: utf-8 -*-

from sqlalchemy import Integer, String, Text, func
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm import aliased
from sqlalchemy.orm.exc import MultipleResultsFound
from sqlalchemy import and_, desc, distinct

from ..helpers import svg_image_url, get_lang
from ..cacher import cacher

from .. import db


# Icon stuff

class IconLang(db.Model):
    __tablename__ = 'icon_lang'

    id = db.Column('id', String(50), db.ForeignKey('icon.id'), primary_key=True)
    lang = db.Column('lang', String(2), primary_key=True)
    name = db.Column('name', Text)
    description = db.Column('description', Text)
    pending = db.Column('pending', Integer)

    def __repr__(self):
        return '<IconLang %s: %r>' % (self.id, self.name)

class Icon(db.Model):
    __tablename__ = 'icon'

    id = db.Column('id', String(50), primary_key=True)
    name = db.Column('name', Text)
    description = db.Column('description', Text)
    group = db.Column('group', String(50))
    order = db.Column('order', Integer)

    def __repr__(self):
        return '<Icon %s: %r>' % (self.id, self.name)

    @hybrid_property
    def svg_url(self):
        return svg_image_url(self.id + '.svg', 'icons')

    @hybrid_property
    def icon(self):
        return self.id

    # Getting filters for this model
    @hybrid_method
    def get_filters(self, **kwargs):
        from .reward import Reward
        from ..projects.models import Project, ProjectCategory
        from ..location.models import ProjectLocation

        filters = []
        # Join Rewards and Project tables for counting
        filters.append(Reward.icon_id == self.id)
        filters.append(Project.id == Reward.project_id)
        # TODO: project status in kwargs
        filters.append(Project.status.in_(Project.SUCCESSFUL_PROJECTS))

        if 'from_date' in kwargs and kwargs['from_date'] is not None:
            filters.append(Project.published >= kwargs['from_date'])
        if 'to_date' in kwargs and kwargs['to_date'] is not None:
            filters.append(Project.published <= kwargs['to_date'])
        if 'project' in kwargs and kwargs['project'] is not None:
            filters.append(Reward.project_id.in_(kwargs['project']))
        if 'node' in kwargs and kwargs['node'] is not None:
            filters.append(Project.node_id.in_(kwargs['node']))
        if 'category' in kwargs and kwargs['category'] is not None:
            filters.append(Project.id == ProjectCategory.project_id)
            filters.append(ProjectCategory.category_id.in_(kwargs['category']))
        if 'location' in kwargs and kwargs['location'] is not None:
            subquery = ProjectLocation.location_subquery(**kwargs['location'])
            filters.append(ProjectLocation.id == Reward.project_id)
            filters.append(ProjectLocation.id.in_(subquery))
        return filters

    @hybrid_method
    @cacher
    def total(self, **kwargs):
        """Total number of icons"""
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
    def list(self, **kwargs):
        """Most used icons (reward type)"""
        from .reward import Reward

        limit = kwargs['limit'] if 'limit' in kwargs else 10
        page = kwargs['page'] if 'page' in kwargs else 0
        filters = self.get_filters(**kwargs)

        cols = [self.id,
                self.name,
                self.description,
                self.group,
                self.order,
                func.count(Reward.project_id).label('total')]

        if 'lang' in kwargs and kwargs['lang'] is not None:

            joins = []
            for l in kwargs['lang']:
                alias = aliased(IconLang)
                cols.append(alias.name.label('name_' + l))
                cols.append(alias.description.label('description_' + l))
                joins.append((alias, and_(alias.id == self.id, alias.lang == l)))
            query = db.session.query(*cols).outerjoin(*joins)
        else:
            query = db.session.query(*cols)

        ret = []
        for u in query.filter(*filters).group_by(self.id) \
                      .order_by(desc('total')) \
                      .offset(page * limit).limit(limit):
            u = u._asdict()
            if 'lang' in kwargs and kwargs['lang'] is not None:
                u['name'] = get_lang(u, 'name', kwargs['lang'])
                u['description'] = get_lang(u, 'description', kwargs['lang'])
                for l in kwargs['lang']:
                    u.pop('name_' + l)
                    u.pop('description_' + l)

            # Return an instance of the Icon class
            ret.append(self(**u))

        return ret
