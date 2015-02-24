# -*- coding: utf-8 -*-

from sqlalchemy import func, Integer, String, Text, Date, DateTime
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from api.helpers import image_url, utc_from_local
from sqlalchemy import asc, or_, distinct

from api import db

from api.models.location import Location, LocationItem

# Reward stuff
class Reward(db.Model):
    __tablename__ = 'reward'

    id = db.Column('id', Integer, primary_key=True)
    project = db.Column('project', String(50), db.ForeignKey('project.id'))
    reward = db.Column('reward', Text)
    type = db.Column('type', String(50))
    amount = db.Column('amount', Integer)
    icon = db.Column('icon', String(50), db.ForeignKey('icon.id'))
    license = db.Column('license', String(50), db.ForeignKey('license.id'))

    def __repr__(self):
        return '<Reward(%d) %s: %s>' % (self.id, self.project[:10], self.title[:50])


    #Filters for this table
    @hybrid_property
    def filters(self):
        return []

    # Getting filters for this model
    @hybrid_method
    def get_filters(self, **kwargs):
        filters = self.filters
        if 'license_type' in kwargs and kwargs['license_type'] is not None:
            filters.append(Reward.type == kwargs['license_type'])
        if 'license' in kwargs and kwargs['license'] is not None:
            filters.append(Reward.license == kwargs['license'])
        if 'from_date' in kwargs and kwargs['from_date'] is not None:
            pass
        if 'to_date' in kwargs and kwargs['to_date'] is not None:
            pass
        if 'project' in kwargs and kwargs['project'] is not None:
            filters.append(Reward.project == kwargs['project'])
        if 'node' in kwargs and kwargs['node'] is not None:
            pass
        if 'category' in kwargs and kwargs['category'] is not None:
            pass
        if 'location' in kwargs and kwargs['location'] is not None:
            # locations_ids = Location.location_ids(**kwargs['location'])
            pass
            # filters.append(LocationItem.locable==1)

        return filters
    @hybrid_method
    def total(self, **kwargs):
        """Total number of rewards"""
        try:
            filters = list(self.get_filters(**kwargs))
            total = db.session.query(func.count(Reward.id)).filter(*filters).scalar()
            if total is None:
                total = 0
            return total
        except MultipleResultsFound:
            return 0
