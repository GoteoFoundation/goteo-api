# -*- coding: utf-8 -*-

from sqlalchemy import func, Integer, String, DateTime, Float
from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy.orm.exc import MultipleResultsFound
from sqlalchemy.sql import select, column

from ..helpers import image_url
from ..decorators import cacher

from .. import db

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

    # Get location subquery using the spherical law of cosines
    # faster than Vincenty and Haversine and done in the bbdd side
    # http://jsperf.com/vincenty-vs-haversine-distance-calculations/2
    #
    #  Does a first "cut" before getting results from the mysql table
    #  as described here:
    #  http://www.movable-type.co.uk/scripts/latlong-db.html
    #
    #  @Cacher cannot be applied here, this only returns a subquery to be executed
    #  from the calling entity
    @hybrid_method
    def location_subquery(self, latitude, longitude, radius, fields=['id']):
        from math import degrees, radians, cos
        R = 6371 # earth's mean radius, km
        latitude = float(latitude)
        longitude = float(longitude)
        radius = float(radius)
        # first-cut bounding box (in degrees)
        maxLat = latitude + degrees(radius/R);
        minLat = latitude - degrees(radius/R);
        # compensate for degrees longitude getting smaller with increasing latitude
        maxLon = longitude + degrees(radius/R/cos(radians(latitude)));
        minLon = longitude - degrees(radius/R/cos(radians(latitude)));
        filters = [self.latitude.between(minLat, maxLat), (self.longitude.between(minLon, maxLon))]
         # acos(sin(:lat)*sin(radians(Lat)) + cos(:lat)*cos(radians(Lat))*cos(radians(Lon)-:lon)) * :R
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
        )
        subquery = db.session.query(self.id,self.latitude,self.longitude,distance.label('distance')).filter(*filters).subquery('FirstCut')
        # print "\n--\n" + subquery + "\n-->--\n"
        sub = select(fields).select_from(subquery).where(distance <= radius)#
        # print sub + "\n--<--\n"
        return sub

    # Vincenty Method, slightly better precision, high cost on querying database
    @hybrid_method
    @cacher
    def location_ids(self, latitude, longitude, radius):
        from geopy.distance import VincentyDistance
        from math import degrees, radians, cos
        R = 6371 # earth's mean radius, km
        latitude = float(latitude)
        longitude = float(longitude)
        radius = float(radius)
        # first-cut bounding box (in degrees)
        maxLat = latitude + degrees(radius/R);
        minLat = longitude - degrees(radius/R);
        # compensate for degrees longitude getting smaller with increasing latitude
        maxLon = longitude + degrees(radius/R/cos(radians(latitude)));
        minLon = longitude - degrees(radius/R/cos(radians(latitude)));
        filters = [Location.latitude.between(minLat, maxLat), (Location.longitude.between(minLon, maxLon))]
        locations = self.query.filter(*filters).all()

        locations = filter(lambda l: VincentyDistance((latitude, longitude), (l.latitude, l.longitude)).km <= radius, locations)
        location_ids = map(lambda l: int(l.id), locations)

        return location_ids

class LocationItem(db.Model):
    __tablename__ = 'location_item'

    id = db.Column('location', Integer, db.ForeignKey('location.id'))
    item = db.Column('item', String(50), primary_key=True)
    type = db.Column('type', String(7), primary_key=True)
    method = db.Column('method', String(50))
    locable = db.Column('locable', Integer)
    info = db.Column('info', String(255))
    modified = db.Column('modified', DateTime)

    def __repr__(self):
        return '<LocationItem: (%s)%s in location %d>' % (self.type, self.item, self.id)
