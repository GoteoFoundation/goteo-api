# -*- coding: utf-8 -*-

from sqlalchemy import func, Integer, String, Date, DateTime
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from api.helpers import image_url, utc_from_local
from sqlalchemy import asc, or_, distinct

from config import config
from api import db

from api.models.invest import Invest
from api.models.message import Message
from api.models.location import Location, LocationItem

# User stuff
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column('id', String(50), primary_key=True)
    name = db.Column('name', String(100))
    avatar = db.Column('avatar', String(255))
    # email = db.Column('email', String(100))
    active = db.Column('active', Integer)
    hide = db.Column('hide', Integer)
    node = db.Column('node', String(50), db.ForeignKey('node.id'))
    created = db.Column('created', Date)
    updated = db.Column('modified', Date)
    # email = db.Column('email', String(255))


    def __repr__(self):
        return '<User %s: %r>' % (self.id, self.name)


    @hybrid_property
    def profile_image_url(self):
        return image_url(self.avatar)

    @hybrid_property
    def date_created(self):
        return utc_from_local(self.created)

    @hybrid_property
    def date_updated(self):
        return utc_from_local(self.updated)

    #Filters for table user
    @hybrid_property
    def filters(self):
        return [User.hide == 0, User.active == 1]

    #Joins for table user
    @hybrid_property
    def joins(self):
        return []

    #Left Joins for table user
    @hybrid_property
    def outerjoins(self):
        return []

    # Getting filters for this model
    @hybrid_method
    def get_filters(self, **kwargs):
        filters = self.filters
        # Filters by goteo node
        if 'node' in kwargs and kwargs['node'] is not None:
            filters.append(User.node.in_(kwargs['node']))
        # Filters by "from date"
        # counting users created after this date
        if 'from_date' in kwargs and kwargs['from_date'] is not None:
            filters.append(User.created >= kwargs['from_date'])
        # Filters by "to date"
        # counting users created before this date
        if 'to_date' in kwargs and kwargs['to_date'] is not None:
            filters.append(User.created <= kwargs['to_date'])
        # Filters by "project"
        # counting attached (invested or collaborated) to some project(s)
        if 'project' in kwargs and kwargs['project'] is not None:
            #TODO: solo usuarios que cuyo pago ha si "exitoso"
            # adding users "invested in"
            sub_invest = db.session.query(Invest.user).filter(Invest.project.in_(kwargs['project']))
            # adding users "collaborated in"
            sub_message = db.session.query(Message.user).filter(Message.project.in_(kwargs['project']))
            filters.append(or_(User.id.in_(sub_invest), User.id.in_(sub_message)))
        # filter by user interests
        if 'category' in kwargs and kwargs['category'] is not None:
            sub_interest = db.session.query(UserInterest.user).filter(UserInterest.interest.in_(kwargs['category']))
            filters.append(User.id.in_(sub_interest))
        #Filter by location
        if 'location' in kwargs and kwargs['location'] is not None:
            #location ids where to search
            locations_ids = Location.location_ids(**kwargs['location'])
            filters.append(LocationItem.type == 'user')
            filters.append(LocationItem.id.in_(locations_ids))
            filters.append(LocationItem.item==User.id)
            filters.append(LocationItem.locable==1)
        #TODO: more filters, like creators, invested, etc
        return filters

    # Getting joins for this models
    @hybrid_method
    def get_joins(self, **kwargs):
        joins = self.joins
        # if 'location' in kwargs and kwargs['location'] is not None:
        #     joins.append((LocationItem, LocationItem.item==User.id))
        return joins

    # Getting joins for this models
    @hybrid_method
    def get_outerjoins(self, **kwargs):
        joins = self.outerjoins
        # if 'project' in kwargs and kwargs['project'] is not None:
        #     joins.append(Message)
        return joins

    @hybrid_method
    def get(self, id):
        """Get a valid user form id"""
        try:
            filters = list(self.filters)
            filters.append(User.id == id)
            return self.query.filter(*filters).one()
        except NoResultFound:
            return None

    @hybrid_method
    def list(self, **kwargs):
        """Get a list of valid users"""
        try:
            limit = kwargs['limit'] if 'limit' in kwargs else 10
            page = kwargs['page'] if 'page' in kwargs else 0
            filters = list(self.get_filters(**kwargs))
            # joins = list(self.get_joins(**kwargs))
            # outerjoins = list(self.get_outerjoins(**kwargs))
            # return self.query.filter(*filters).join(*joins).outerjoin(*outerjoins).order_by(asc(User.id)).offset(page * limit).limit(limit)
            return self.query.filter(*filters).order_by(asc(User.id)).offset(page * limit).limit(limit)
        except NoResultFound:
            return []

    @hybrid_method
    def total(self, **kwargs):
        """Returns the total number of valid users"""
        try:
            filters = list(self.get_filters(**kwargs))
            # joins = list(self.get_joins(**kwargs))
            # outerjoins = list(self.get_outerjoins(**kwargs))
            # count = db.session.query(func.count(distinct(User.id))).filter(*filters).join(*joins).outerjoin(*outerjoins).scalar()
            count = db.session.query(func.count(distinct(User.id))).filter(*filters).scalar()
            if count is None:
                count = 0
            return count
        except MultipleResultsFound:
            return 0


#User roles
class UserRole(db.Model):
    __tablename__ = 'user_role'

    user_id = db.Column('user_id', String(50), db.ForeignKey('user.id'), primary_key=True)
    role_id = db.Column('role_id', String(50), primary_key=True)
    node_id = db.Column('node_id', String(50), db.ForeignKey('node.id'))

    def __repr__(self):
        return '<UserRole %s: %s>' % (self.user_id, self.role_id)


#Api keys
class UserApi(db.Model):
    __tablename__ = 'user_api'

    user = db.Column('user_id', String(50), db.ForeignKey('user.id'), primary_key=True)
    key = db.Column('key', String(50))
    expiration_date = db.Column('expiration_date', DateTime)

    def __repr__(self):
        return '<UserApi: %s %s (%s)>' % (self.user, self.key, self.expiration_date)

# User interest
class UserInterest(db.Model):
    __tablename__ = 'user_interest'

    user = db.Column('user', String(50), db.ForeignKey('user.id'), primary_key=True)
    interest = db.Column('interest', Integer, db.ForeignKey('category.id'), primary_key=True)

    def __repr__(self):
        return '<UserInterest from %s to project %s>' % (self.user, self.project)
