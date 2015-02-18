# -*- coding: utf-8 -*-

from sqlalchemy import func, Integer, String, Text, Date, DateTime
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from api.helpers import image_url, utc_from_local
from sqlalchemy import asc, or_, distinct

from api.helpers import debug_time, svg_image_url
from config import config
from api import db

from api.models.location import Location, LocationItem

# DEBUG
if config.debug:
    db.session.query = debug_time(db.session.query)

# Reward stuff
class Reward(db.Model):
    __tablename__ = 'reward'

    id = db.Column('id', Integer, primary_key=True)
    project = db.Column('project', String(50), db.ForeignKey('project.id'))
    reward = db.Column('reward', Text)
    type = db.Column('type', String(50))
    amount = db.Column('amount', Integer)
    icon = db.Column('icon', String(50))

    def __repr__(self):
        return '<Reward(%d) %s: %s>' % (self.id, self.project[:10], self.title[:50])
