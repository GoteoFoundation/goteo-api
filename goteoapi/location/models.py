# -*- coding: utf-8 -*-

from sqlalchemy import func, String, DateTime, Float, Boolean, Integer
from flask.ext.restful import fields
from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql import select, column

from ..cacher import cacher

from .. import db

location_resource_fields = {
    "city": fields.String,
    "region": fields.String,
    "country": fields.String,
    "country_code": fields.String,
    "latitude": fields.Float,
    "longitude": fields.Float,
    "radius": fields.Integer
}


class ItemLocation(object):
    """This class can be used as base for the implementing SQL tables"""

    id = db.Column('id', String(50), primary_key=True)
    latitude = db.Column('latitude', Float)
    longitude = db.Column('longitude', Float)
    radius = db.Column('radius', Integer)
    method = db.Column('method', String(50))
    locable = db.Column('locable', Boolean)
    city = db.Column('city', String(255))
    region = db.Column('region', String(255))
    country = db.Column('country', String(255))
    country_code = db.Column('country_code', String(2))
    info = db.Column('info', String(255))
    modified = db.Column('modified', DateTime)

    def __repr__(self):
        return '<ItemLocation: (%s) in %f,%f>' % (
            self.id, self.latitude, self.longitude)

    @hybrid_method
    @cacher
    def get(self, id_, locable=False):
        """Get a valid Location Item from id_"""
        try:
            if not locable:
                return self.query.get(id_)
            return self.query \
                       .filter(self.id == id_, self.locable == locable) \
                       .one()
        except NoResultFound:
            return None

    # Get location subquery using the spherical law of cosines
    # faster than Vincenty and Haversine and done in the bbdd side
    # http://jsperf.com/vincenty-vs-haversine-distance-calculations/2
    #
    #  Does a first "cut" before getting results from the mysql table
    #  as described here:
    #  http://www.movable-type.co.uk/scripts/latlong-db.html
    #
    #  @Cacher cannot be applied here,
    #  this only returns a subquery to be executed
    #  from the calling entity
    @hybrid_method
    def location_subquery(self,
                          latitude,
                          longitude,
                          radius,
                          locable_only=False, fields=['id']):
        from math import degrees, radians, cos

        R = 6371  # earth's mean radius, km
        latitude = float(latitude)
        longitude = float(longitude)
        radius = float(radius)
        # first-cut bounding box (in degrees)
        maxLat = latitude + degrees(radius / R)
        minLat = latitude - degrees(radius / R)
        # compensate for degrees longitude
        # getting smaller with increasing latitude
        maxLon = longitude + degrees(radius / R / cos(radians(latitude)))
        minLon = longitude - degrees(radius / R / cos(radians(latitude)))
        filters = [self.latitude.between(minLat, maxLat),
                   self.longitude.between(minLon, maxLon)]
        if locable_only:
            filters.append(self.locable == True)
        rlat = radians(latitude)
        rlng = radians(longitude)
        distance = (
            func.acos(
                func.sin(rlat)
                * func.sin(func.radians(column('latitude')))
                + func.cos(rlat)
                * func.cos(func.radians(column('latitude')))
                * func.cos(func.radians(column('longitude')) - rlng)
            ) * R
        ).label('distance')
        subquery = db.session.query(
            self.id,
            self.latitude,
            self.longitude,
            self.method,
            self.city,
            self.country,
            self.country_code,
            self.modified,
            distance) \
            .filter(*filters) \
            .subquery('FirstCut')
        sub = select(map(column, fields)) \
            .select_from(subquery) \
            .where(distance <= radius)
        return sub

    # Vincenty Method, slightly better precision,
    # high cost on querying database
    # @hybrid_method
    # @cacher
    # def location_ids(self, latitude, longitude, radius, locable_only=False):
    #     from geopy.distance import VincentyDistance
    #     from math import degrees, radians, cos

    #     R = 6371 # earth's mean radius, km
    #     latitude = float(latitude)
    #     longitude = float(longitude)
    #     radius = float(radius)
    #     # first-cut bounding box (in degrees)
    #     maxLat = latitude + degrees(radius/R)
    #     minLat = longitude - degrees(radius/R)
    #     # compensate for degrees longitude getting smaller
    #     # with increasing latitude
    #     maxLon = longitude + degrees(radius/R/cos(radians(latitude)))
    #     minLon = longitude - degrees(radius/R/cos(radians(latitude)))
    #     filters = [self.latitude.between(minLat, maxLat),
    #               self.longitude.between(minLon, maxLon)]
    #     if locable_only:
    #         filters.append(self.locable == True)

    #     locations = self.query.filter(*filters).all()

    #     locations = filter(lambda l: VincentyDistance((latitude, longitude),
    #                   (l.latitude, l.longitude)).km <= radius, locations)
    #     location_ids = map(lambda l: int(l.id), locations)

    #     return location_ids


#####################
# IMPLEMENTATIONS
#####################


class UserLocation(db.Model, ItemLocation):
    """User location particular case"""
    __tablename__ = 'user_location'

    id = db.Column('id', String(50),
                   db.ForeignKey('user.id'), primary_key=True)

    def __repr__(self):
        return '<UserLocation: (%s) in %f,%f>' % (
            self.id, self.latitude, self.longitude)

    # Overide use to set default locable = True
    @hybrid_method
    @cacher
    def get(self, id_, locable=True):
        """Get a valid Location Item from id"""
        return super(ItemLocation, self).get(id_, locable)


class ProjectLocation(db.Model, ItemLocation):
    """Project location particular case"""
    __tablename__ = 'project_location'

    id = db.Column('id', String(50),
                   db.ForeignKey('project.id'), primary_key=True)

    def __repr__(self):
        return '<ProjectLocation: (%s) in %f,%f>' % (
            self.id, self.latitude, self.longitude)


class CallLocation(db.Model, ItemLocation):
    """Call location particular case"""
    __tablename__ = 'call_location'

    id = db.Column('id', String(50),
                   db.ForeignKey('call.id'), primary_key=True)

    def __repr__(self):
        return '<CallLocation: (%s) in %f,%f>' % (
            self.id, self.latitude, self.longitude)


class InvestLocation(db.Model, ItemLocation):
    """Invest location particular case"""
    __tablename__ = 'invest_location'

    id = db.Column('id', Integer,
                   db.ForeignKey('invest.id'), primary_key=True)

    def __repr__(self):
        return '<InvestLocation: (%s) in %f,%f>' % (
            self.id, self.latitude, self.longitude)
