# -*- coding: utf-8 -*-

#from flask.ext.sqlalchemy import Pagination
from sqlalchemy import func, and_, distinct, asc, Integer, String, Text, Date
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm import aliased,relationship
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from ..helpers import image_url, utc_from_local, get_lang
from ..base_resources import AbstractLang
from ..cacher import cacher

from .. import db

class CallLang(AbstractLang, db.Model):
    __tablename__ = 'call_lang'

    id = db.Column('id', String(50), db.ForeignKey('call.id'), primary_key=True)
    lang = db.Column('lang', String(2), primary_key=True)
    name_lang = db.Column('name', String(100))
    subtitle_lang = db.Column('subtitle', Text)
    description_lang = db.Column('description', Text)
    legal_lang = db.Column('legal', Text)
    whom_lang = db.Column('whom', Text)
    apply_lang = db.Column('apply', Text)
    dossier_lang = db.Column('dossier', Text)
    tweet_lang = db.Column('tweet', Text)
    resources_lang = db.Column('resources', Text)
    pending = db.Column('pending', Integer)
    # call = relationship('Call', back_populates='call_langs')

    def __repr__(self):
        return '<CallLang %s(%s): %r>' % (self.id, self.lang, self.name_lang)

class Call(db.Model):
    __tablename__ = 'call'

    #CALL STATUS IDs
    STATUS_PENDING   = 0
    STATUS_EDITING    = 1
    STATUS_REVIEWING  = 2
    STATUS_APPLYING   = 3
    STATUS_PUBLISHED  = 4
    STATUS_SUCCEEDED  = 5
    STATUS_EXPIRED    = 6
    STATUS_STR = ('pending', 'editing', 'reviewing', 'applying', 'published', 'succeeded', 'expired')

    id = db.Column('id', String(50), primary_key=True)
    name = db.Column('name', Text)
    amount = db.Column('amount', Integer)
    subtitle = db.Column('subtitle', Text)
    description = db.Column('description', Text)
    owner = db.Column('owner', String(50))
    whom = db.Column('whom', Text)
    apply = db.Column('apply', Text)
    legal = db.Column('legal', Text)
    dossier = db.Column('dossier', Text)
    tweet = db.Column('tweet', Text)
    resources = db.Column('resources', Text)
    lang = db.Column('lang', String(2))
    status = db.Column('status', Integer)
    created = db.Column('created', Date)
    updated = db.Column('updated', Date)
    opened = db.Column('opened', Date)
    published = db.Column('published', Date)
    success = db.Column('success', Date)
    closed = db.Column('closed', Date)
    logo = db.Column('logo', String(255))
    image = db.Column('image', String(255))
    backimage = db.Column('backimage', String(255))
    # call_langs = relationship("CallLang", order_by=CallLang.id, back_populates="call")

    def __repr__(self):
        return '<Call %s: %s>' % (self.id, self.name)

    @hybrid_property
    def image_url(self):
        return image_url(self.image, size="big")

    @hybrid_property
    def backimage_url(self):
        return image_url(self.backimage, size="big")

    @hybrid_property
    def logo_url(self):
        return image_url(self.logo, size="medium")

    @hybrid_property
    def date_created(self):
        return utc_from_local(self.created)

    @hybrid_property
    def date_updated(self):
        return utc_from_local(self.updated)

    @hybrid_property
    def date_opened(self):
        return utc_from_local(self.opened)

    @hybrid_property
    def date_published(self):
        return utc_from_local(self.published)

    @hybrid_property
    def date_succeeded(self):
        return utc_from_local(self.success)

    @hybrid_property
    def date_closed(self):
        return utc_from_local(self.closed)

    @hybrid_property
    def status_string(self):
        return self.STATUS_STR[self.status]

    #Filters for this table
    @hybrid_property
    def filters(self):
        return [self.status > self.STATUS_EDITING]

    # Getting filters for this model
    @hybrid_method
    def get_filters(self, **kwargs):
        filters = self.filters
        if 'from_date' in kwargs and kwargs['from_date'] is not None:
            filters.append(self.opened >= kwargs['from_date'])
        # Filters by "to date"
        # counting license created before this date
        if 'to_date' in kwargs and kwargs['to_date'] is not None:
            filters.append(self.opened <= kwargs['to_date'])

        return filters

    @hybrid_method
    @cacher
    def get(self, call_id):
        """Get a valid matchfunding form id"""
        try:
            filters = self.get_filters()
            filters.append(self.id == call_id)
            return self.query.filter(*filters).one()
        except NoResultFound:
            return None

    @hybrid_method
    @cacher
    def list(self, **kwargs):
        """Get a list of valid matchfunding calls"""
        try:
            limit = kwargs['limit'] if 'limit' in kwargs else 10
            page = kwargs['page'] if 'page' in kwargs else 0
            filters = self.get_filters(**kwargs)
            # In case of requiring languages, a LEFT JOIN must be generated
            if 'lang' in kwargs and kwargs['lang'] is not None:
                ret = []
                for u in CallLang.get_query(kwargs['lang']) \
                                 .filter(*filters).order_by(asc(self.opened)) \
                                 .offset(page * limit).limit(limit):
                    ret.append(CallLang.get_translated_object(u._asdict(), kwargs['lang']))
                return ret
            return self.query.distinct().filter(*filters) \
                                        .order_by(asc(self.opened)) \
                                        .offset(page * limit).limit(limit).all()
        except NoResultFound:
            return []

    @hybrid_method
    @cacher
    def total(self, **kwargs):
        """Total number of matchfunding calls"""
        try:
            filters = self.get_filters(**kwargs)
            total = db.session.query(func.count(distinct(self.id))).filter(*filters).scalar()
            if total is None:
                total = 0
            return total
        except MultipleResultsFound:
            return 0

    @hybrid_method
    @cacher
    def pledged_total(self, **kwargs):
        """Capital Riego de Goteo (funds from institutions and companies added to the Capital Riego) """
        try:
            filters = list(self.get_filters(**kwargs))
            total = db.session.query(func.sum(Call.amount)).filter(*filters).scalar()
            if total is None:
                total = 0
            return total
        except MultipleResultsFound:
            return 0
