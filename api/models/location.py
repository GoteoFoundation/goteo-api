# -*- coding: utf-8 -*-

from sqlalchemy import func, Integer, String, DateTime, Float
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from api.helpers import image_url, utc_from_local
from sqlalchemy import asc
from api import db

class Location(db.Model):
    __tablename__ = 'location'

    id = db.Column('id', Integer, primary_key=True)
    city = db.Column('city', String(255))
    region = db.Column('region', String(255))
    country = db.Column('country', String(255))
    country_code = db.Column('country_code', String(2))
    longitude = db.Column('longitude', Float)
    latitude = db.Column('latitude', Float)
    valid = db.Column('valid', Integer)
    modified = db.Column('modified', DateTime)

    def __repr__(self):
        return '<Location(%d) %s, %s (%s)>' % (self.id, self.city, self.region, self.country)


class LocationItem(db.Model):
    __tablename__ = 'location_item'

    id = db.Column('location', Integer)
    item = db.Column('item', String(50), primary_key=True)
    type = db.Column('type', String(7), primary_key=True)
    method = db.Column('method', String(50))
    locable = db.Column('locable', Integer)
    info = db.Column('info', String(255))
    modified = db.Column('modified', DateTime)

    def __repr__(self):
        return '<LocationItem: (%s)%s in location %d>' % (self.type, self.item, self.id)
