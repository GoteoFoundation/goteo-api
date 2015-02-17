# -*- coding: utf-8 -*-

#from flask.ext.sqlalchemy import Pagination
from sqlalchemy import func, Integer, String, Text, Date, DateTime, Float
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from api.helpers import image_url, utc_from_local
from sqlalchemy import asc
from api import db

class Project(db.Model):
    __tablename__ = 'project'

    #PROJECT STATUS IDs
    STATUS_REJECTED    = 0
    STATUS_EDITING     = 1
    STATUS_REVIEWING   = 2
    STATUS_IN_CAMPAIGN = 3
    STATUS_FUNDED      = 4
    STATUS_FULLFILED   = 5 # 'Caso de exito'
    STATUS_UNFUNDED    = 6 # proyecto fallido

    id = db.Column('id', String(50), primary_key=True)
    owner = db.Column('owner', String(50), db.ForeignKey('user.id'))
    name = db.Column('name', Text)
    category = db.Column('category', String(50), db.ForeignKey('category.id'))
    minimum = db.Column('mincost', Integer)
    optimum = db.Column('maxcost', Integer)
    #subtitle = db.Column('subtitle', String(255))
    status = db.Column('status', Integer)
    #created = db.Column('created', Date)
    date_passed = db.Column('passed', Date)
    date_updated = db.Column('updated', Date)
    date_published = db.Column('published', Date)
    date_closed = db.Column('closed', Date)
    node = db.Column('node', String(50), db.ForeignKey('node.id'))
    # total_funding
    # active_date
    # rewards
    # platform
    #aportes = db.relationship('Invest', backref='project')

    def __repr__(self):
        return '<Project %s: %s>' % (self.id, self.name)




class ProjectCategory(db.Model):
    __tablename__ = 'project_category'

    project = db.Column('project', String(50), db.ForeignKey('project.id'), primary_key=True)
    category = db.Column('category', Integer, db.ForeignKey('category.id'), primary_key=True)

    def __repr__(self):
        return '<Category %s>' % (self.name)

