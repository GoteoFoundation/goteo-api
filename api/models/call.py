# -*- coding: utf-8 -*-

#from flask.ext.sqlalchemy import Pagination
from sqlalchemy import func, Integer, String, Text, Date
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm.exc import MultipleResultsFound

from ..decorators import cacher
from .. import db
from ..helpers import utc_from_local

class Call(db.Model):
    __tablename__ = 'call'

    #CALL STATUS IDs
    STATUS_CANCELED   = 0
    STATUS_EDITING    = 1
    STATUS_REVIEWING  = 2
    STATUS_APPLYING   = 3
    STATUS_PUBLISHING = 4
    STATUS_COMPLETED  = 5
    STATUS_EXPIRED    = 6

    id = db.Column('id', String(50), primary_key=True)
    name = db.Column('name', Text)
    amount = db.Column('amount', Integer)
    owner = db.Column('owner', String(50))
    status = db.Column('status', Integer)
    opened = db.Column('opened', Date)
    published = db.Column('published', Date)

    def __repr__(self):
        return '<Call %s: %s>' % (self.id, self.name)


    @hybrid_property
    def date_opened(self):
        return utc_from_local(self.opened)

    @hybrid_property
    def date_published(self):
        return utc_from_local(self.published)

    #Filters for this table
    @hybrid_property
    def filters(self):
        return [self.status > self.STATUS_EDITING]

    # Getting filters for this model
    @hybrid_method
    def get_filters(self, **kwargs):
        filters = self.filters
        if 'from_date' in kwargs and kwargs['from_date'] is not None:
            filters.append(self.opened >= kwargs['from_date'])
        # Filters by "to date"
        # counting license created before this date
        if 'to_date' in kwargs and kwargs['to_date'] is not None:
            filters.append(self.opened <= kwargs['to_date'])

        return filters

    @hybrid_method
    @cacher
    def pledged_total(self, **kwargs):
        """Capital Riego de Goteo (funds from institutions and companies added to the Capital Riego) """
        try:
            filters = list(self.get_filters(**kwargs))
            total = db.session.query(func.sum(Call.amount)).filter(*filters).scalar()
            if total is None:
                total = 0
            return total
        except MultipleResultsFound:
            return 0
