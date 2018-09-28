# -*- coding: utf-8 -*-

from sqlalchemy import func, Integer, String, Text
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy import distinct

from ..helpers import image_url,asset_url
from ..base_resources import AbstractLang
from ..cacher import cacher

from .. import db


class SocialCommitmentLang(AbstractLang, db.Model):
    __tablename__ = 'social_commitment_lang'

    id = db.Column('id', Integer,
                   db.ForeignKey('social_commitment.id'), primary_key=True)
    lang = db.Column('lang', String(2), primary_key=True)
    name = db.Column('name', Text)
    description = db.Column('description', Text)
    pending = db.Column('pending', Integer)

    def __repr__(self):
        return '<SocialCommitmentLang %s(%s): %r>' % (self.id, self.lang, self.name)


class SocialCommitment(db.Model):
    __tablename__ = 'social_commitment'

    id = db.Column('id', Integer, primary_key=True)
    name = db.Column('name', Text)
    icon = db.Column('icon', String(255))
    description = db.Column('description', Text)

    def __repr__(self):
        return '<SocialCommitment %s: %r>' % (self.id, self.name)

    @hybrid_property
    def icon_url(self):
        if(self.icon):
            return image_url(self.icon, size="medium")
        else:
            return asset_url('img/social-commitment/square/' + str(self.id) + '.png')

    @hybrid_property
    def icon_url_big(self):
        return image_url(self.icon, size="big")

    # Filters for table SocialCommitment
    @hybrid_property
    def filters(self):
        return [self.name != '']

    # Getting filters for this model
    @hybrid_method
    def get_filters(self, **kwargs):

        from ..projects.models import Project
        from ..location.models import ProjectLocation
        from ..calls.models import CallProject

        filters = self.filters
        # Join project table if filters
        for i in ('node', 'call', 'from_date', 'to_date', 'project', 'location'):
            if i in kwargs and kwargs[i] is not None:
                filters.append(self.id == ProjectSocialCommitment.SocialCommitment_id)
                filters.append(Project.id == ProjectSocialCommitment.project_id)
                filters.append(Project.status.in_(Project.PUBLISHED_PROJECTS))
                break

        # Filters by goteo node
        if 'node' in kwargs and kwargs['node'] is not None:
            filters.append(Project.node_id.in_(kwargs['node']))
        # Filters by "from date"
        # counting SocialCommitment created after this date
        if 'from_date' in kwargs and kwargs['from_date'] is not None:
            filters.append(Project.published >= kwargs['from_date'])
        # Filters by "to date"
        # counting SocialCommitment created before this date
        if 'to_date' in kwargs and kwargs['to_date'] is not None:
            filters.append(Project.published <= kwargs['to_date'])
        # Filters by "project"
        # counting attached (invested or collaborated) to some project(s)
        if 'project' in kwargs and kwargs['project'] is not None:
            filters.append(Project.id.in_(kwargs['project']))
        # counting attached (invested or collaborated) to some project(s)
        # involving call
        if 'call' in kwargs and kwargs['call'] is not None:
            filters.append(ProjectSocialCommitment.project_id == CallProject.project_id)
            filters.append(CallProject.call_id.in_(kwargs['call']))
        # filter by SocialCommitment interests
        if 'SocialCommitment' in kwargs and kwargs['SocialCommitment'] is not None:
            filters.append(self.id.in_(kwargs['SocialCommitment']))
        # Filter by location
        if 'location' in kwargs and kwargs['location'] is not None:
            filters.append(ProjectLocation.id == ProjectSocialCommitment.project_id)
            subquery = ProjectLocation.location_subquery(**kwargs['location'])
            filters.append(ProjectLocation.id.in_(subquery))

        return filters

    @hybrid_method
    @cacher
    def get(self, id_):
        """Get a valid SocialCommitment from id"""
        try:
            filters = list(self.filters)
            filters.append(self.id == id_)
            return self.query.filter(*filters).one()
        except NoResultFound:
            return None

    @hybrid_method
    @cacher
    def list(self, **kwargs):
        """Get a list of valid SocialCommitment"""
        try:
            filters = list(self.get_filters(**kwargs))
            # In case of requiring languages, a LEFT JOIN must be generated
            if 'lang' in kwargs and kwargs['lang'] is not None:
                ret = []
                for u in SocialCommitmentLang.get_query(kwargs['lang']) \
                                     .filter(*filters):
                    ret.append(SocialCommitmentLang.get_translated_object(
                        u._asdict(), kwargs['lang']))
                return ret
            # No langs, normal query
            return self.query.distinct().filter(*filters).all()

        except NoResultFound:
            return []

    @hybrid_method
    @cacher
    def total(self, **kwargs):
        """Returns the total number of valid SocialCommitment"""
        try:
            filters = list(self.get_filters(**kwargs))
            count = db.session.query(func.count(distinct(self.id))) \
                              .filter(*filters).scalar()
            if count is None:
                count = 0
            return count
        except MultipleResultsFound:
            return 0
