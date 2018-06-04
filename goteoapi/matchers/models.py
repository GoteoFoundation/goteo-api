# -*- coding: utf-8 -*-

from sqlalchemy import func, distinct, asc, Integer, String, Text, Date, DateTime, Boolean
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from ..helpers import image_url, utc_from_local, matcher_url
from ..base_resources import AbstractLang
from ..cacher import cacher

from .. import db


class MatcherLang(AbstractLang, db.Model):
    __tablename__ = 'matcher_lang'

    id = db.Column('id', String(50),
                   db.ForeignKey('matcher.id'), primary_key=True)
    lang = db.Column('lang', String(2), primary_key=True)
    name = db.Column('name', String(255))
    terms = db.Column('terms', Text)
    # pending = db.Column('pending', Integer)
    Matcher = relationship('Matcher', back_populates='Translations')

    def __repr__(self):
        return '<MatcherLang %s(%s): %r>' % (self.id, self.lang, self.name)


class Matcher(db.Model):
    __tablename__ = 'matcher'

    id = db.Column('id', String(50), primary_key=True)
    name = db.Column('name', Text)
    user_id = db.Column('owner', String(50), db.ForeignKey('user.id'))
    User = relationship("User", lazy='joined')  # Eager loading for catching
    terms = db.Column('terms', Text)
    # Total available amount
    amount_available = db.Column('amount', Integer, nullable=False)
    # Total Amount committed on projects
    amount_committed = db.Column('used', Integer, nullable=False)
    # Total Amount provided by end users (not matchfunding)
    amount_peers = db.Column('crowd', Integer, nullable=False)
    # Selected projects
    projects_active = db.Column('projects', Integer, nullable=False)
    vars = db.Column('vars', Text)
    lang = db.Column('lang', String(2))
    created = db.Column('created', Date)
    modified = db.Column('modified_at', DateTime)
    active = db.Column('active', Boolean)
    logo = db.Column('logo', String(255))
    matcher_location = db.Column('matcher_location', String(255))
    Translations = relationship(
        "MatcherLang",
        # primaryjoin="and_(Matcher.id==MatcherLang.id, MatcherLang.pending==0)",
        primaryjoin="and_(Matcher.id==MatcherLang.id)",
        back_populates="Matcher", lazy='joined')  # Eager loading for catching
    Users = relationship(
        "MatcherUser",
        primaryjoin="Matcher.id==MatcherUser.matcher_id",
        back_populates="Matcher", lazy='joined')  # Eager loading for catching
    Projects = relationship(
        "MatcherProject",
        primaryjoin="Matcher.id==MatcherProject.matcher_id",
        back_populates="Matcher", lazy='joined')  # Eager loading for catching

    def __repr__(self):
        return '<Matcher %s: %s>' % (self.id, self.name)

    @hybrid_property
    def owner(self):
        return self.user_id

    @hybrid_property
    def owner_name(self):
        # Manually get the User object if not exists
        if not self.User:
            from ..users.models import User
            self.User = User.get(self.user_id)
        return self.User.name

    @hybrid_property
    def matcher_url(self):
        return matcher_url(self.id)

    @hybrid_property
    def logo_url(self):
        return image_url(self.logo, size="medium")

    @hybrid_property
    def amount_remaining(self):
        return self.amount_available - self.amount_committed

    @hybrid_property
    def date_created(self):
        return utc_from_local(self.created)

    @hybrid_property
    def date_updated(self):
        return utc_from_local(self.modified)

    @hybrid_property
    def projects_total(self):
        return self.projects_count()


    # Getting filters for this model
    @hybrid_method
    def get_filters(self, **kwargs):
        # from ..location.models import MatcherLocation
        from ..projects.models import Project, ProjectCategory

        filters = [self.active == True]

        if 'from_date' in kwargs and kwargs['from_date'] is not None:
            filters.append(self.created >= kwargs['from_date'])
        # Filters by "to date"
        # counting license created before this date
        if 'to_date' in kwargs and kwargs['to_date'] is not None:
            filters.append(self.created <= kwargs['to_date'])
        if 'project' in kwargs and kwargs['project'] is not None:
            filters.append(self.id == MatcherProject.matcher_id)
            filters.append(MatcherProject.project_id.in_(kwargs['project']))
        if 'category' in kwargs and kwargs['category'] is not None:
            filters.append(self.id == MatcherProject.matcher_id)
            filters.append(
                MatcherProject.project_id == ProjectCategory.project_id)
            filters.append(ProjectCategory.category_id.in_(kwargs['category']))
        if 'matcher' in kwargs and kwargs['matcher'] is not None:
            filters.append(self.id.in_(kwargs['matcher']))
        if 'node' in kwargs and kwargs['node'] is not None:
            filters.append(self.id == MatcherProject.matcher_id)
            filters.append(MatcherProject.project_id == Project.id)
            filters.append(Project.node_id.in_(kwargs['node']))

        return filters

    @hybrid_method
    @cacher
    def get(self, matcher_id):
        """Get a valid matchfunding form id"""
        try:
            filters = self.get_filters()
            filters.append(self.id == matcher_id)
            return self.query.filter(*filters).one()
        except NoResultFound:
            return None

    @hybrid_method
    @cacher
    def list(self, **kwargs):
        """Get a list of valid matchfunding matchers"""
        try:
            limit = kwargs['limit'] if 'limit' in kwargs else 10
            page = kwargs['page'] if 'page' in kwargs else 0
            filters = self.get_filters(**kwargs)
            # In case of requiring languages, a LEFT JOIN must be generated
            if 'lang' in kwargs and kwargs['lang'] is not None:
                ret = []
                for u in MatcherLang.get_query(kwargs['lang']) \
                                 .filter(*filters).order_by(asc(self.created)) \
                                 .offset(page * limit).limit(limit):
                    ret.append(MatcherLang.get_translated_object(u._asdict(),
                                                              kwargs['lang']))
                return ret
            # No langs, normal query
            return self.query.distinct().filter(*filters) \
                                        .order_by(asc(self.created)) \
                                        .offset(page * limit) \
                                        .limit(limit).all()
        except NoResultFound:
            return []

    @hybrid_method
    @cacher
    def total(self, **kwargs):
        """Total number of matchfunding matchers"""
        try:
            filters = self.get_filters(**kwargs)
            total = db.session.query(func.count(distinct(self.id))) \
                      .filter(*filters).scalar()
            if total is None:
                total = 0
            return total
        except MultipleResultsFound:
            return 0

    @hybrid_method
    @cacher
    def pledged_total(self, **kwargs):
        """Capital Riego de Goteo
        (funds from institutions and companies added to the Capital Riego)
        """
        try:
            filters = list(self.get_filters(**kwargs))
            total = db.session.query(func.sum(Matcher.amount_total)) \
                      .filter(*filters).scalar()
            if total is None:
                total = 0
            return total
        except MultipleResultsFound:
            return 0


    @hybrid_method
    @cacher
    def users_list(self):
        from ..users.models import User
        users = []
        for s in self.Users:
            users.append(s)
        try:
            filters = [self.id == MatcherUser.matcher_id, MatcherUser.user_id==User.id]
            users = User.query.filter(*filters).all()
            return users
        except NoResultFound:
            return []

    @hybrid_method
    @cacher
    def projects_list(self, status=None):
        from ..users.models import Project
        projects = []
        for s in self.Projects:
            projects.append(s)
        try:
            filters = [self.id==MatcherProject.matcher_id,
                       MatcherProject.status==status,
                       MatcherProject.project_id==Project.id]
            projects = Project.query.filter(*filters).all()
            return projects
        except NoResultFound:
            return []

    @hybrid_method
    @cacher
    def projects_count(self, status=None):
        """Total number of projects on this matcher"""
        try:
            filters = []
            if status:
                filters.append(MatcherProject.status==status)
            total = db.session.query(func.count(MatcherProject.project_id)) \
                              .filter(*filters).scalar()
            if total is None:
                total = 0
            return total
        except MultipleResultsFound:
            return 0

# Matcher projects
class MatcherProject(db.Model):
    __tablename__ = 'matcher_project'

    matcher_id = db.Column('matcher_id', String(50),
                        db.ForeignKey('matcher.id'), primary_key=True)
    project_id = db.Column('project_id', String(50),
                           db.ForeignKey('project.id'), primary_key=True)
    status = db.Column('status', String(10))
    Matcher = relationship('Matcher', back_populates='Projects')

    def __repr__(self):
        return '<MatcherProject from %s to project %s>' % (
            self.matcher_id, self.project_id)

# Matcher users
class MatcherUser(db.Model):
    __tablename__ = 'matcher_user'

    matcher_id = db.Column('matcher_id', String(50),
                        db.ForeignKey('matcher.id'), primary_key=True)
    user_id = db.Column('user_id', String(50),
                        db.ForeignKey('user.id'), primary_key=True)
    pool = db.Column('pool', Boolean)
    admin = db.Column('admin', Boolean)
    Matcher = relationship('Matcher', back_populates='Users')


    def __repr__(self):
        return '<MatcherUser from %s to user %s>' % (
            self.matcher_id, self.user_id)

