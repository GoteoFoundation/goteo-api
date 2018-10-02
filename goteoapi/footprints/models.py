# -*- coding: utf-8 -*-

from sqlalchemy import func, Integer, String, Text
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.orm import relationship
from sqlalchemy import distinct

from ..helpers import image_url,asset_url,as_list
from ..base_resources import AbstractLang
from ..cacher import cacher

from .. import db


class FootprintLang(AbstractLang, db.Model):
    __tablename__ = 'footprint_lang'

    id = db.Column('id', Integer,
                   db.ForeignKey('footprint.id'), primary_key=True)
    lang = db.Column('lang', String(2), primary_key=True)
    name = db.Column('name', Text)
    description = db.Column('description', Text)
    pending = db.Column('pending', Integer)
    Footprint = relationship('Footprint', back_populates='Translations')

    def __repr__(self):
        return '<FootprintLang %s(%s): %r>' % (self.id, self.lang, self.name)


class FootprintCategory(db.Model):
    __tablename__ = 'category_footprint'

    footprint_id = db.Column('footprint_id', Integer,
                   db.ForeignKey('footprint.id'), primary_key=True)
    category_id = db.Column('category_id', Integer,
                   db.ForeignKey('category.id'), primary_key=True)

    def __repr__(self):
        return '<FootprintCategory %s(%s): %r>' % (self.footprint_id, self.category_id)

class FootprintSocialCommitment(db.Model):
    __tablename__ = 'social_commitment_footprint'

    footprint_id = db.Column('footprint_id', Integer,
                   db.ForeignKey('footprint.id'), primary_key=True)
    social_commitment_id = db.Column('social_commitment_id', Integer,
                   db.ForeignKey('social_commitment.id'), primary_key=True)

    def __repr__(self):
        return '<FootprintSocialCommitment %s(%s): %r>' % (self.footprint_id, self.social_commitment_id)


class Footprint(db.Model):
    __tablename__ = 'footprint'

    id = db.Column('id', Integer, primary_key=True)
    name = db.Column('name', Text)
    icon = db.Column('icon', String(255))
    description = db.Column('description', Text)
    # Categories = relationship("Category",
    #     primaryjoin="Footprint.id==Category.footprint_id",
    #     back_populates="Footprint", lazy="joined")
    Translations = relationship(
        "FootprintLang",
        primaryjoin="Footprint.id==FootprintLang.id",
        back_populates="Footprint", lazy='joined')  # Eager loading for catching

    def __repr__(self):
        return '<Footprint %s: %r>' % (self.id, self.name)

    @hybrid_property
    def sdgs(self):
        from ..sdgs.models import Sdg
        return Sdg.list(footprint=self.id)

    @hybrid_property
    def categories(self):
        from ..categories.models import Category
        return Category.list(footprint=self.id)

    @hybrid_property
    def social_commitments(self, lang=None):
        from ..social_commitments.models import SocialCommitment
        return SocialCommitment.list(footprint=self.id, lang=lang)

    @hybrid_property
    def icon_url(self):
        if(self.icon):
            return image_url(self.icon, size="medium")
        else:
            return asset_url('img/footprint/' + str(self.id) + '.svg')

    @hybrid_property
    def icon_url_big(self):
        return image_url(self.icon, size="big")

    # Filters for table Footprint
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
                filters.append(self.id == Project.footprint_id)
                filters.append(Project.status.in_(Project.PUBLISHED_PROJECTS))
                break

        # Filters by goteo node
        if 'node' in kwargs and kwargs['node'] is not None:
            filters.append(Project.node_id.in_(as_list(kwargs['node'])))
        # Filters by "from date"
        # counting Footprint created after this date
        if 'from_date' in kwargs and kwargs['from_date'] is not None:
            filters.append(Project.published >= kwargs['from_date'])
        # Filters by "to date"
        # counting Footprint created before this date
        if 'to_date' in kwargs and kwargs['to_date'] is not None:
            filters.append(Project.published <= kwargs['to_date'])
        # Filters by "project"
        # counting attached (invested or collaborated) to some project(s)
        if 'project' in kwargs and kwargs['project'] is not None:
            filters.append(Project.id.in_(as_list(kwargs['project'])))
        # counting attached (invested or collaborated) to some project(s)
        # involving call
        if 'call' in kwargs and kwargs['call'] is not None:
            filters.append(Project.id == CallProject.project_id)
            filters.append(CallProject.call_id.in_(as_list(kwargs['call'])))
        # filter by SocialCommitment
        if 'social_commitment' in kwargs and kwargs['social_commitment'] is not None:
            filters.append(self.id.in_(as_list(kwargs['social_commitment'])))
        # filter by Category
        if 'category' in kwargs and kwargs['category'] is not None:
            filters.append(self.id == FootprintCategory.footprint_id)
            filters.append(FootprintCategory.category_id.in_(as_list(kwargs['category'])))
        # Filter by location
        if 'location' in kwargs and kwargs['location'] is not None:
            filters.append(ProjectLocation.id == Project.id)
            subquery = ProjectLocation.location_subquery(**kwargs['location'])
            filters.append(ProjectLocation.id.in_(subquery))

        return filters

    @hybrid_method
    @cacher
    def get(self, id_, lang=None):
        """Get a valid Footprint from id"""
        try:
            filters = list(self.filters)
            filters.append(self.id == id_)
            # This model does not have lang embeded in the main table
            if lang:
                trans = FootprintLang.get_query(lang).filter(*filters).one()
                return FootprintLang.get_translated_object(
                        trans._asdict(), lang)
            return self.query.filter(*filters).one()
        except NoResultFound:
            return None

    @hybrid_method
    @cacher
    def list(self, **kwargs):
        """Get a list of valid Footprint"""
        try:
            filters = list(self.get_filters(**kwargs))
            # In case of requiring languages, a LEFT JOIN must be generated
            if 'lang' in kwargs and kwargs['lang'] is not None:
                ret = []
                for u in FootprintLang.get_query(kwargs['lang']) \
                                     .filter(*filters):
                    ret.append(FootprintLang.get_translated_object(
                        u._asdict(), kwargs['lang']))
                return ret
            # No langs, normal query
            return self.query.distinct().filter(*filters).all()

        except NoResultFound:
            return []

    @hybrid_method
    @cacher
    def total(self, **kwargs):
        """Returns the total number of valid Footprint"""
        try:
            filters = list(self.get_filters(**kwargs))
            count = db.session.query(func.count(distinct(self.id))) \
                              .filter(*filters).scalar()
            if count is None:
                count = 0
            return count
        except MultipleResultsFound:
            return 0
