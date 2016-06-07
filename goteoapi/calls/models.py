# -*- coding: utf-8 -*-

from sqlalchemy import func, distinct, asc, Integer, String, Text, Date
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from ..helpers import image_url, utc_from_local, call_url
from ..base_resources import AbstractLang
from ..cacher import cacher
from ..invests.models import Invest

from .. import db


class CallLang(AbstractLang, db.Model):
    __tablename__ = 'call_lang'

    id = db.Column('id', String(50), db.ForeignKey('call.id'), primary_key=True)
    lang = db.Column('lang', String(2), primary_key=True)
    name = db.Column('name', String(100))
    subtitle = db.Column('subtitle', Text)
    description = db.Column('description', Text)
    legal = db.Column('legal', Text)
    whom = db.Column('whom', Text)
    applies = db.Column('apply', Text)
    dossier = db.Column('dossier', Text)
    tweet = db.Column('tweet', Text)
    resources = db.Column('resources', Text)
    pending = db.Column('pending', Integer)
    Call = relationship('Call', back_populates='Translations')

    def __repr__(self):
        return '<CallLang %s(%s): %r>' % (self.id, self.lang, self.name)


class Call(db.Model):
    __tablename__ = 'call'

    #CALL STATUS IDs
    STATUS_PENDING = 0
    STATUS_EDITING = 1
    STATUS_REVIEWING = 2
    STATUS_APPLYING = 3
    STATUS_PUBLISHED = 4
    STATUS_SUCCEEDED = 5
    STATUS_EXPIRED = 6
    STATUS_STR = ('pending', 'editing', 'reviewing', 'applying', 'published', 'succeeded', 'expired')

    PUBLIC_CALLS = [STATUS_APPLYING, STATUS_PUBLISHED, STATUS_SUCCEEDED, STATUS_EXPIRED]

    SCOPES_STR = ('', 'local', 'regional', 'national', 'global')

    id = db.Column('id', String(50), primary_key=True)
    name = db.Column('name', Text)
    subtitle = db.Column('subtitle', Text)
    description = db.Column('description', Text)
    user_id = db.Column('owner', String(50), db.ForeignKey('user.id'))
    User = relationship("User", lazy='joined') # Eager loading to allow catching
    whom = db.Column('whom', Text)
    applies = db.Column('apply', Text)
    legal = db.Column('legal', Text)
    dossier = db.Column('dossier', Text)
    amount_available = db.Column('amount', Integer, nullable=False) # Total available amount
    amount_remaining = db.Column('rest', Integer, nullable=False) # Total Amount remaining to distribute
    amount_committed = db.Column('used', Integer, nullable=False) # Total Amount committed on projects
    projects_total = db.Column('num_projects', Integer, nullable=False) # Selected projects
    projects_applied = db.Column('applied', Integer, nullable=False) # Applied projects succeeded
    projects_active = db.Column('running_projects', Integer, nullable=False) # Applied projects in active campaign
    projects_succeeded = db.Column('success_projects', Integer, nullable=False) # Applied successful projects
    tweet = db.Column('tweet', Text)
    resources = db.Column('resources', Text)
    lang = db.Column('lang', String(2))
    status = db.Column('status', Integer, nullable=False)
    scope = db.Column('scope', Integer, nullable=False)
    created = db.Column('created', Date)
    updated = db.Column('updated', Date)
    opened = db.Column('opened', Date)
    published = db.Column('published', Date)
    success = db.Column('success', Date)
    closed = db.Column('closed', Date)
    logo = db.Column('logo', String(255))
    image = db.Column('image', String(255))
    backimage = db.Column('backimage', String(255))
    facebook = db.Column('fbappid', String(255))
    call_location = db.Column('call_location', String(255))
    Translations = relationship("CallLang",
                                primaryjoin="and_(Call.id==CallLang.id, CallLang.pending==0)",
                                back_populates="Call", lazy='joined') # Eager loading to allow catching

    def __repr__(self):
        return '<Call %s: %s>' % (self.id, self.name)

    @hybrid_property
    def amount_peers(self):
        return float(Invest.pledged_total(not_method=Invest.METHOD_DROP, call=self.id))

    @hybrid_property
    def owner(self):
        return self.user_id

    @hybrid_property
    def owner_name(self):
        return self.User.name

    @hybrid_property
    def description_short(self):
        return self.subtitle

    @hybrid_property
    def call_url(self):
        return call_url(self.id)

    @hybrid_property
    def facebook_url(self):
        return self.facebook

    @hybrid_property
    def image_url(self):
        return image_url(self.image, size="medium")

    @hybrid_property
    def image_url_big(self):
        return image_url(self.image, size="big")

    @hybrid_property
    def image_background_url(self):
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

    @hybrid_property
    def scope_string(self):
        return self.SCOPES_STR[self.scope]

    # Getting filters for this model
    @hybrid_method
    def get_filters(self, **kwargs):
        from ..location.models import CallLocation
        from ..projects.models import Project, ProjectCategory

        filters = [self.status.in_(self.PUBLIC_CALLS)]

        if 'from_date' in kwargs and kwargs['from_date'] is not None:
            filters.append(self.opened >= kwargs['from_date'])
        # Filters by "to date"
        # counting license created before this date
        if 'to_date' in kwargs and kwargs['to_date'] is not None:
            filters.append(self.opened <= kwargs['to_date'])
        if 'project' in kwargs and kwargs['project'] is not None:
            filters.append(self.id == CallProject.call_id)
            filters.append(CallProject.project_id.in_(kwargs['project']))
        if 'category' in kwargs and kwargs['category'] is not None:
            filters.append(self.id == CallProject.call_id)
            filters.append(CallProject.project_id == ProjectCategory.project_id)
            filters.append(ProjectCategory.category_id.in_(kwargs['category']))
        if 'node' in kwargs and kwargs['node'] is not None:
            filters.append(self.id == CallProject.call_id)
            filters.append(CallProject.project_id == Project.id)
            filters.append(Project.node_id.in_(kwargs['node']))
        if 'location' in kwargs and kwargs['location'] is not None:
            subquery = CallLocation.location_subquery(**kwargs['location'])
            filters.append(CallLocation.id == self.id)
            filters.append(CallLocation.id.in_(subquery))
        if 'loc_status' in kwargs and kwargs['loc_status'] is not None:
            if kwargs['loc_status'] == 'located':
                filters.append(self.id.in_(db.session.query(CallLocation.id).subquery()))
            if kwargs['loc_status'] == 'unlocated':
                filters.append(~self.id.in_(db.session.query(CallLocation.id).subquery()))

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
            # No langs, normal query
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
            total = db.session.query(func.sum(Call.amount_available)).filter(*filters).scalar()
            if total is None:
                total = 0
            return total
        except MultipleResultsFound:
            return 0


# Call projects
class CallProject(db.Model):
    __tablename__ = 'call_project'

    call_id = db.Column('call', String(50), db.ForeignKey('call.id'), primary_key=True)
    project_id = db.Column('project', String(50), db.ForeignKey('project.id'), primary_key=True)

    def __repr__(self):
        return '<CallProject from %s to project %s>' % (self.call_id, self.project_id)
