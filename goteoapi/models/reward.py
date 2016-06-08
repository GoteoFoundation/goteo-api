# -*- coding: utf-8 -*-

from sqlalchemy import func, Integer, String, Text, Boolean
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from sqlalchemy import asc, distinct
from sqlalchemy.orm import relationship

from ..cacher import cacher
from ..helpers import svg_image_url
from ..projects.models import Project, ProjectCategory
from ..licenses.models import License, LicenseLang
from ..models.icon import Icon
from ..base_resources import AbstractLang

from .. import db


class RewardLang(AbstractLang, db.Model):
    __tablename__ = 'reward_lang'

    id = db.Column('id', Integer, db.ForeignKey('reward.id'), primary_key=True)
    lang = db.Column('lang', String(2), primary_key=True)
    name = db.Column('reward', Text)
    description = db.Column('description', Text)
    other = db.Column('other', String(255))
    pending = db.Column('pending', Integer)
    Reward = relationship('Reward',
                          back_populates='Translations',
                          lazy='joined')  # Eager loading to allow catching

    def __repr__(self):
        return '<RewardLang %s(%s): %r>' % (self.id, self.lang, self.name)

    @hybrid_property
    def License(self):
        return LicenseLang.get(self.Reward.license_id, lang=self.lang)

    @hybrid_property
    def license(self):
        return self.License.id

    @hybrid_property
    def license_name(self):
        return self.License.name

    @hybrid_property
    def license_description(self):
        return self.License.description

    @hybrid_property
    def license_url(self):
        return self.License.url


# Reward stuff
class Reward(db.Model):
    __tablename__ = 'reward'

    id = db.Column('id', Integer, primary_key=True)
    project_id = db.Column('project', String(50), db.ForeignKey('project.id'))
    name = db.Column('reward', String(50))
    description = db.Column('description', Text)
    type = db.Column('type', String(50))
    other = db.Column('other', String(255))
    amount = db.Column('amount', Integer)
    units = db.Column('units', Integer)
    fulsocial = db.Column('fulsocial', Boolean)
    url = db.Column('url', String(255))
    icon_id = db.Column('icon', String(50), db.ForeignKey('icon.id'))
    license_id = db.Column('license', String(50), db.ForeignKey('license.id'))
    order = db.Column('order', Integer)
    License = relationship("License",
                           lazy="joined")  # Eager loading to allow catching
    Icon = relationship("Icon",
                        lazy="joined")  # Eager loading to allow catching
    Translations = relationship(
        "RewardLang",
        primaryjoin="and_(Reward.id==RewardLang.id, RewardLang.pending==0)",
        back_populates="Reward", lazy='joined')  # Eager loading for catching

    def __repr__(self):
        return '<Reward(%d) %s[%s]: %s>' % (
            self.id, self.project_id, self.type, self.name)

    @hybrid_property
    def icon_url(self):
        return svg_image_url(self.icon_id + '.svg', 'icons')

    @hybrid_property
    def license(self):
        return self.License.id

    @hybrid_property
    def license_name(self):
        return self.License.name

    @hybrid_property
    def license_description(self):
        return self.License.description

    @hybrid_property
    def license_url(self):
        return self.License.url

    @hybrid_property
    def license_svg_url(self):
        return self.License.svg_url

    # Getting filters for this model
    @hybrid_method
    def get_filters(self, **kwargs):
        from ..location.models import ProjectLocation

        filters = []
        prj_filters = (
            'node', 'from_date', 'to_date', 'project', 'category', 'location')
        # Join project table if filters
        for i in prj_filters:
            if i in kwargs and kwargs[i] is not None:
                filters.append(Project.id == self.project_id)
                filters.append(Project.status.in_(Project.PUBLISHED_PROJECTS))
        if 'icon' in kwargs and kwargs['icon'] is not None:
            filters.append(self.icon_id == kwargs['icon'])
        if 'license_type' in kwargs and kwargs['license_type'] is not None:
            filters.append(self.type == kwargs['license_type'])
        if 'license' in kwargs and kwargs['license'] is not None:
            filters.append(self.license_id.in_(kwargs['license']))
        if 'from_date' in kwargs and kwargs['from_date'] is not None:
            filters.append(Project.published >= kwargs['from_date'])
        if 'to_date' in kwargs and kwargs['to_date'] is not None:
            filters.append(Project.published <= kwargs['to_date'])
        if 'project' in kwargs and kwargs['project'] is not None:
            filters.append(self.project_id.in_(kwargs['project']))
        if 'node' in kwargs and kwargs['node'] is not None:
            filters.append(Project.node_id.in_(kwargs['node']))
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
            return self.query.distinct() \
                       .filter(*filters) \
                       .order_by(asc(self.order), asc(self.amount)) \
                       .offset(page * limit).limit(limit).all()
        except NoResultFound:
            return []

    @hybrid_method
    @cacher
    def list_by_project(self, project_id, lang=None):
        """Get a list of valid rewards for project"""
        try:
            filters = [self.project_id == project_id]
            if lang:
                filters.append(RewardLang.id == self.id)
                filters.append(RewardLang.lang == lang)
                return RewardLang.query.distinct() \
                                 .filter(*filters) \
                                 .order_by(asc(self.order), asc(self.amount)) \
                                 .all()
            return self.query.distinct() \
                       .filter(*filters) \
                       .order_by(asc(self.order), asc(self.amount)).all()
        except NoResultFound:
            return []

    @hybrid_method
    @cacher
    def total(self, **kwargs):
        """Total number of rewards"""
        try:
            filters = list(self.get_filters(**kwargs))
            total = db.session.query(func.count(distinct(self.id))) \
                      .filter(*filters).scalar()
            if total is None:
                total = 0
            return total
        except MultipleResultsFound:
            return 0
