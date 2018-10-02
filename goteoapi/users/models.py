# -*- coding: utf-8 -*-
from sqlalchemy import func, Integer, String, Date, DateTime, Boolean, Text
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy import asc, desc, and_, or_, distinct
from sqlalchemy.orm import aliased, relationship

from ..cacher import cacher
from ..helpers import image_url, utc_from_local, user_url, get_lang, as_list
from ..base_resources import AbstractLang

from ..categories.models import Category, CategoryLang
from ..invests.models import Invest
from ..projects.models import Project
from ..calls.models import CallProject
from ..models.node import Node
from ..models.message import Message
from ..location.models import UserLocation
from hashlib import sha1
from passlib.context import CryptContext

from .. import db


class UserLang(AbstractLang, db.Model):
    __tablename__ = 'user_lang'

    id = db.Column('id', String(50),
                   db.ForeignKey('user.id'), primary_key=True)
    lang = db.Column('lang', String(2), primary_key=True)
    name = db.Column('name', String(100))
    User = relationship('User', back_populates='Translations')

    def __repr__(self):
        return '<UserLang %s(%s): %r>' % (self.id, self.lang, self.name)


# User stuff
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column('id', String(50), primary_key=True)
    password_hash = db.Column('password', String(255))
    name = db.Column('name', String(100))
    about = db.Column('about', Text)
    avatar = db.Column('avatar', String(255))
    email = db.Column('email', String(255))
    active = db.Column('active', Boolean)
    hide = db.Column('hide', Boolean)
    node_id = db.Column('node', String(50), db.ForeignKey(Node.id))
    created = db.Column('created', Date)
    updated = db.Column('modified', Date)
    lang = db.Column('lang', String(2))
    Translations = relationship("UserLang",
                                back_populates="User",
                                lazy='joined')  # Eager loading for catching

    def __repr__(self):
        return '<User %s: %r>' % (self.id, self.name)

    @hybrid_property
    def node(self):
        return self.node_id

    @hybrid_property
    def profile_image_url(self):
        return image_url(self.avatar)

    @hybrid_property
    def profile_url(self):
        return user_url(self.id)

    @hybrid_property
    def date_created(self):
        return utc_from_local(self.created)

    @hybrid_property
    def date_updated(self):
        return utc_from_local(self.updated)

    @hybrid_property
    def amount_public_invested(self):
        return float(Invest.pledged_total(user=self.id, is_anonymous=False))

    @hybrid_property
    def amount_private_invested(self):
        return float(Invest.pledged_total(user=self.id, is_anonymous=True))

    @hybrid_property
    def projects_public_invested(self):
        return Project.total(user=self.id, is_anonymous=False)

    @hybrid_property
    def projects_published(self):
        return Project.total(owner=self.id)

    @hybrid_property
    def projects_collaborated(self):
        return Message.projects_total(user=self.id)

    @hybrid_method
    def get_context(self):
        myctx = CryptContext(schemes=["bcrypt"], bcrypt__default_rounds=12)
        return myctx

    @hybrid_method
    def hash_password(self, password):
        """Hashes password. Passswords are pre-sha1 encoded"""
        sha = sha1(password.encode('utf-8'))
        self.password_hash = self.get_context().encrypt(sha.hexdigest())
        return self.password_hash

    @hybrid_method
    def verify_password(self, password):
        """Verifies password. Passswords are pre-sha1 encoded"""

        sha = sha1(password.encode('utf-8'))
        try:
            (ok, update) = self.get_context() \
                               .verify_and_update(sha.hexdigest(),
                                                  self.password_hash)
        except ValueError:
            print('old ' + self.password_hash)
            # Old plain SHA-1 database stored password
            ok = sha.hexdigest() == self.password_hash
            update = self.get_context().encrypt(self.password_hash)
        if ok and update:
            # update database
            self.password_hash = update
        return ok

    @hybrid_property
    def filters(self):
        return [self.hide == 0, self.active == 1]

    # Getting filters for this model
    @hybrid_method
    def get_filters(self, **kwargs):
        "Return filters to be used"
        from ..projects.models import ProjectCategory
        from ..sdgs.models import SdgSocialCommitment, SdgCategory
        from ..footprints.models import FootprintSocialCommitment, FootprintCategory

        filters = self.filters
        if 'unsubscribed' in kwargs and kwargs['unsubscribed'] is not None:
            filters = [or_(self.hide == 1, self.active == 0)]

        # Filters by goteo node
        if 'node' in kwargs and kwargs['node'] is not None:
            # Old method: does not seems to be very reliable
            # filters.append(self.node_id.in_(as_list(kwargs['node'])))
            #
            sub_invest1 = db.session.query(Invest.user_id).filter(
                Invest.user_id == self.id,
                Invest.project_id == Project.id,
                Invest.status.in_(Invest.VALID_INVESTS),
                Project.node_id.in_(as_list(kwargs['node'])))
            sub_project1 = db.session.query(Project.user_id).filter(
                Project.user_id == self.id,
                Project.node_id.in_(as_list(kwargs['node'])))
            # sub_message1 = db.session.query(Message.user_id).filter(
            #     Message.user_id == self.id,
            #     Message.project_id == Project.id,
            #     Project.node_id.in_(as_list(kwargs['node'])))
            filters.append(or_(self.id.in_(sub_invest1),
                self.id.in_(sub_project1)
                # , self.id.in_(sub_message1)
                ))
        if 'call' in kwargs and kwargs['call'] is not None:
            sub_invest2 = db.session.query(Invest.user_id).filter(
                Invest.user_id == self.id,
                Invest.call_id.in_(as_list(kwargs['call'])),
                Invest.status.in_(Invest.VALID_INVESTS))
            sub_project2 = db.session.query(Project.user_id).filter(
                Project.user_id == self.id,
                Project.id == CallProject.project_id,
                CallProject.call_id.in_(as_list(kwargs['call'])))
            filters.append(or_(self.id.in_(sub_invest2),
                self.id.in_(sub_project2)))
        # Filters by "from date"
        # counting users created after this date
        if 'from_date' in kwargs and kwargs['from_date'] is not None:
            filters.append(self.created >= kwargs['from_date'])
        # Filters by "to date"
        # counting users created before this date
        if 'to_date' in kwargs and kwargs['to_date'] is not None:
            filters.append(self.created <= kwargs['to_date'])
        # Filters by "project"
        # counting attached (invested or collaborated) to some project(s)
        if 'project' in kwargs and kwargs['project'] is not None:
            # adding users "invested in"
            sub_invest = db.session.query(Invest.user_id).filter(
                Invest.project_id.in_(as_list(kwargs['project'])),
                Invest.status.in_(Invest.VALID_INVESTS))
            # adding users "collaborated in"
            sub_message = db.session.query(Message.user_id) \
                            .filter(Message.project_id.in_(as_list(kwargs['project'])))
            filters.append(or_(self.id.in_(sub_invest),
                               self.id.in_(sub_message)))
        # filter by social commitments
        if 'social_commitment' in kwargs and kwargs['social_commitment'] is not None:
            # adding users "invested in"
            filters.append(self.id == Invest.user_id)
            filters.append(Invest.project_id == Project.id)
            filters.append(Invest.status.in_(Invest.VALID_INVESTS))
            filters.append(Project.social_commitment_id.in_(as_list(kwargs['social_commitment'])))

        # filter by sdgs
        if 'sdg' in kwargs and kwargs['sdg'] is not None:
            filters.append(self.id == Invest.user_id)
            filters.append(Invest.project_id == Project.id)
            filters.append(Invest.status.in_(Invest.VALID_INVESTS))

            sub1 = db.session.query(SdgSocialCommitment.social_commitment_id) \
                .filter(SdgSocialCommitment.sdg_id.in_(as_list(kwargs['sdg'])))
            filters.append(Project.social_commitment_id.in_(sub1))
            # Search using categories but highly inefficient:
            # and1 = and_(Project.social_commitment_id != None,
            #     Project.social_commitment_id.in_(sub1))
            # sub2 = db.session.query(ProjectCategory.project_id) \
            #     .filter(ProjectCategory.project_id == SdgCategory.category_id, SdgCategory.sdg_id.in_(as_list(kwargs['sdg'])))
            # and2 = and_(Project.social_commitment_id == None,
            #     Project.id.in_(sub2))
            # filters.append(or_(and1, and2))
        # filter by footprints
        if 'footprint' in kwargs and kwargs['footprint'] is not None:
            filters.append(self.id == Invest.user_id)
            filters.append(Invest.project_id == Project.id)
            filters.append(Invest.status.in_(Invest.VALID_INVESTS))

            sub1 = db.session.query(FootprintSocialCommitment.social_commitment_id) \
                .filter(FootprintSocialCommitment.footprint_id.in_(as_list(kwargs['footprint'])))
            filters.append(Project.social_commitment_id.in_(sub1))
            # Search using categories but highly inefficient:
            # and1 = and_(Project.social_commitment_id != None,
            #     Project.social_commitment_id.in_(sub1))
            # sub2 = db.session.query(ProjectCategory.project_id) \
            #     .filter(ProjectCategory.project_id == FootprintCategory.category_id, FootprintCategory.footprint_id.in_(as_list(kwargs['footprint'])))
            # and2 = and_(Project.social_commitment_id == None,
            #     Project.id.in_(sub2))
            # filters.append(or_(and1, and2))
        # filter by user interests
        if 'category' in kwargs and kwargs['category'] is not None:
            sub_interest = db.session.query(UserInterest.user_id) \
                             .filter(UserInterest.category_id
                                                 .in_(as_list(kwargs['category'])))
            filters.append(self.id.in_(sub_interest))
        # Filter by location
        if 'location' in kwargs and kwargs['location'] is not None:
            # location ids where to search
            subquery = UserLocation.location_subquery(**kwargs['location'])
            filters.append(UserLocation.id.in_(subquery))
            filters.append(UserLocation.id == self.id)

        # TODO: more filters, like creators, invested, etc
        return filters

    @hybrid_method
    @cacher
    def get(self, user_id):
        """Get a valid user form id"""
        try:
            filters = list(self.filters)
            filters.append(self.id == user_id)
            return self.query.filter(*filters).one()
        except NoResultFound:
            return None

    @hybrid_method
    @cacher
    def list(self, **kwargs):
        """Get a list of valid users"""
        try:
            limit = kwargs['limit'] if 'limit' in kwargs else 10
            page = kwargs['page'] if 'page' in kwargs else 0
            filters = list(self.get_filters(**kwargs))
            # In case of requiring languages, a LEFT JOIN must be generated
            if 'lang' in kwargs and kwargs['lang'] is not None:
                ret = []
                for u in UserLang.get_query(kwargs['lang']) \
                                 .filter(*filters).order_by(asc(self.id)) \
                                 .offset(page * limit).limit(limit):
                    ret.append(UserLang.get_translated_object(u._asdict(),
                                                              kwargs['lang']))
                return ret

            # No langs, normal query
            return self.query.distinct().filter(*filters) \
                                        .order_by(asc(self.id)) \
                                        .offset(page * limit) \
                                        .limit(limit) \
                                        .all()
        except NoResultFound:
            return []

    @hybrid_method
    @cacher
    def total(self, **kwargs):
        """Returns the total number of valid users"""
        try:
            filters = list(self.get_filters(**kwargs))
            count = db.session.query(func.count(distinct(self.id))) \
                      .filter(*filters).scalar()
            if count is None:
                count = 0
            return count
        except MultipleResultsFound:
            return 0

    @hybrid_method
    @cacher
    def donors_by_project(self, project_id, **kwargs):
        """Get a list of valid donors for project"""
        try:
            limit = kwargs['limit'] if 'limit' in kwargs else 10
            page = kwargs['page'] if 'page' in kwargs else 0
            del kwargs['project']
            filters = list(self.get_filters(**kwargs))
            filters.append(Invest.status.in_(Invest.VALID_INVESTS))
            filters.append(Invest.user_id == self.id)
            filters.append(Invest.project_id == project_id)
            # return self.query.distinct() \
            # .filter(*filters) \
            # .order_by(asc(self.id)) \
            # .offset(page * limit).limit(limit).all()
            return [d._asdict() for d in db.session.query(
                Invest.anonymous,
                self.id,
                self.name,
                self.avatar,
                self.active,
                self.hide,
                self.node_id,
                self.created,
                self.updated)
                .filter(*filters) \
                # .order_by(asc(self.id)) \
                .group_by(self.id) \
                .offset(page * limit) \
                .limit(limit)
            ]
        except NoResultFound:
            return []

    @hybrid_method
    @cacher
    def donors_by_project_total(self, project_id, **kwargs):
        """Returns the total number of valid of valid donors for project"""
        try:
            del kwargs['project']
            filters = list(self.get_filters(**kwargs))
            filters.append(Invest.status.in_(Invest.VALID_INVESTS))
            filters.append(Invest.user_id == self.id)
            filters.append(Invest.project_id == project_id)
            count = db.session.query(func.count(distinct(self.id))) \
                      .filter(*filters).scalar()
            if count is None:
                count = 0
            return count
        except MultipleResultsFound:
            return 0


# User roles
class UserRole(db.Model):
    __tablename__ = 'user_role'

    user_id = db.Column('user_id', String(50),
                        db.ForeignKey('user.id'), primary_key=True)
    role_id = db.Column('role_id', String(50), primary_key=True)
    node_id = db.Column('node_id', String(50), db.ForeignKey('node.id'))

    def __repr__(self):
        return '<UserRole %s: %s>' % (self.user_id, self.role_id)


# Api keys
class UserApi(db.Model):
    __tablename__ = 'user_api'

    user_id = db.Column('user_id', String(50),
                        db.ForeignKey('user.id'), primary_key=True)
    key = db.Column('key', String(50))
    expiration_date = db.Column('expiration_date', DateTime)

    def __repr__(self):
        return '<UserApi: %s %s (%s)>' % (
            self.user_id, self.key, self.expiration_date)


# User interest
class UserInterest(db.Model):
    __tablename__ = 'user_interest'

    user_id = db.Column('user', String(50),
                        db.ForeignKey('user.id'), primary_key=True)
    category_id = db.Column('interest', Integer,
                            db.ForeignKey('category.id'), primary_key=True)

    def __repr__(self):
        return '<UserInterest from %s to category %s>' % (
            self.user_id, self.category_id)

    # Getting filters for this model
    @hybrid_method
    def get_filters(self, **kwargs):
        filters = [Category.name != '']  # para categorias
        if 'from_date' in kwargs and kwargs['from_date'] is not None:
            filters.append(Invest.date_created >= kwargs['from_date'])
            filters.append(Invest.user_id == self.user_id)
            filters.append(Invest.status.in_(Invest.VALID_INVESTS))
        if 'to_date' in kwargs and kwargs['to_date'] is not None:
            filters.append(Invest.date_created <= kwargs['to_date'])
            filters.append(Invest.user_id == self.user_id)
            filters.append(Invest.status.in_(Invest.VALID_INVESTS))
        if 'project' in kwargs and kwargs['project'] is not None:
            filters.append(Invest.project_id.in_(as_list(kwargs['project'])))
            filters.append(Invest.user_id == self.user_id)
            filters.append(Invest.status.in_(Invest.VALID_INVESTS))
        if 'node' in kwargs and kwargs['node'] is not None:
            # TODO: project_node o invest_node?
            # Does not seems to be realiable
            filters.append(User.id == self.user_id)
            filters.append(User.node_id.in_(as_list(kwargs['node'])))
        if 'call' in kwargs and kwargs['call'] is not None:
            filters.append(Invest.call_id.in_(as_list(kwargs['call'])))
            filters.append(Invest.user_id == self.user_id)
            filters.append(Invest.status.in_(Invest.VALID_INVESTS))
        if 'category' in kwargs and kwargs['category'] is not None:
            filters.append(self.category_id.in_(as_list(kwargs['category'])))
        if 'location' in kwargs and kwargs['location'] is not None:
            # Filtra por la localización del usuario
            subquery = UserLocation.location_subquery(**kwargs['location'])
            filters.append(self.user_id == UserLocation.id)
            filters.append(UserLocation.id.in_(subquery))
        return filters

    # Categories list
    @hybrid_method
    @cacher
    def categories(self, **kwargs):
        # In case of requiring languages, a LEFT JOIN must be generated
        cols = [func.count(self.user_id).label('total'),
                Category.id,
                Category.name]
        filters = list(self.get_filters(**kwargs))
        # In case of requiring languages, a LEFT JOIN must be generated
        if 'lang' in kwargs and kwargs['lang'] is not None:
            joins = []
            for l in kwargs['lang']:
                alias = aliased(CategoryLang)
                cols.append(alias.name.label('name_' + l))
                joins.append((alias, and_(alias.id == Category.id,
                                          alias.lang == l)))
            query = db.session.query(*cols) \
                      .join(Category, Category.id == self.category_id) \
                      .outerjoin(*joins)
        else:
            query = db.session.query(*cols) \
                      .join(Category, Category.id == self.category_id)
        ret = []

        for u in query.filter(*filters).group_by(self.category_id)\
                      .order_by(desc(func.count(self.user_id))):
            u = u._asdict()
            if 'lang' in kwargs and kwargs['lang'] is not None:
                u['name'] = get_lang(u, 'name', kwargs['lang'])
                for l in kwargs['lang']:
                    u.pop('name_' + l)
            ret.append(Category(**u))

        return ret
