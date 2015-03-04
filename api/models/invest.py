# -*- coding: utf-8 -*-

from sqlalchemy import func, Integer, String, DateTime, Float, Date
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from api.helpers import image_url, utc_from_local
from sqlalchemy import asc
from api.models.location import Location, LocationItem
from api.models.project import ProjectCategory
from api import db

class Invest(db.Model):
    __tablename__ = 'invest'

    METHOD_PAYPAL = 'paypal'
    METHOD_TPV    = 'tpv'
    METHOD_CASH   = 'cash'
    METHOD_DROP   = 'drop'

    #INVEST STATUS IDs
    STATUS_PROCESSING = -1
    STATUS_PENDING    = 0
    STATUS_CHARGED    = 1
    STATUS_CANCELED   = 2
    STATUS_PAID       = 3
    STATUS_RETURNED   = 4
    STATUS_RELOCATED  = 5

    id = db.Column('id', Integer, primary_key=True)
    user = db.Column('user', String(50), db.ForeignKey('user.id'))
    project = db.Column('project', String(50), db.ForeignKey('project.id'))
    status = db.Column('status', Integer)
    amount = db.Column('amount', Integer)
    method = db.Column('method', String(20))
    date_invested = db.Column('invested', Date)
    date_charged = db.Column('charged', Date)
    resign = db.Column('resign', Integer)
    call = db.Column('call', String(50))

    def __repr__(self):
        return '<Invest %d: %s (%d EUR)>' % (self.id, self.project, self.amount)

    #Filters for this table
    @hybrid_property
    def filters(self):
        return []

    # Getting filters for this model
    @hybrid_method
    def get_filters(self, **kwargs):
        filters = self.filters
        if 'from_date' in kwargs and kwargs['from_date'] is not None:
            filters.append(Invest.date_invested >= kwargs['from_date'])
        if 'to_date' in kwargs and kwargs['to_date'] is not None:
            filters.append(Invest.date_invested <= kwargs['to_date'])
        if 'project' in kwargs and kwargs['project'] is not None:
            filters.append(Invest.project.in_(kwargs['project']))
        if 'node' in kwargs and kwargs['node'] is not None:
            filters.append(Invest.id == InvestNode.invest_id)
            filters.append(InvestNode.invest_node.in_(kwargs['node']))
        if 'category' in kwargs and kwargs['category'] is not None:
            filters.append(Invest.project == ProjectCategory.project)
            filters.append(ProjectCategory.category.in_(kwargs['category']))

        if 'location' in kwargs and kwargs['location'] is not None:
            filters.append(Invest.user == LocationItem.item)
            filters.append(LocationItem.type == 'user')
            subquery = Location.location_subquery(**kwargs['location'])
            filters.append(LocationItem.id.in_(subquery))
            # filters.append(LocationItem.locable==1)
            #

        return filters

    @hybrid_method
    def pledged_total(self, **kwargs):
        """Total amount of money (€) raised by Goteo"""
        try:
            filters = list(self.get_filters(**kwargs))
            filters.append(Invest.status.in_([Invest.STATUS_PENDING,
                                              Invest.STATUS_CHARGED,
                                              Invest.STATUS_PAID,
                                              Invest.STATUS_RETURNED]))
            total = db.session.query(func.sum(Invest.amount)).filter(*filters).scalar()
            if total is None:
                total = 0
            return total
        except MultipleResultsFound:
            return 0

    @hybrid_method
    def pledged_successful(self, **kwargs):
        """Total amount of money (€) raised by Goteo only on successful projects"""
        try:
            filters = list(self.get_filters(**kwargs))
            filters.append(Invest.status.in_([Invest.STATUS_CHARGED,
                                              Invest.STATUS_PAID]))
            total = db.session.query(func.sum(Invest.amount)).filter(*filters).scalar()
            if total is None:
                total = 0
            return total
        except MultipleResultsFound:
            return 0

    @hybrid_method
    def pledged_failed(self, **kwargs):
        """Total amount of money (€) raised by Goteo and returned due project failure"""
        try:
            filters = list(self.get_filters(**kwargs))
            filters.append(Invest.status.in_([Invest.STATUS_PENDING,
                                              Invest.STATUS_RETURNED]))
            total = db.session.query(func.sum(Invest.amount)).filter(*filters).scalar()
            if total is None:
                total = 0
            return total
        except MultipleResultsFound:
            return 0


class InvestNode(db.Model):
    __tablename__ = 'invest_node'

    user_id = db.Column('user_id', String(50))
    user_node = db.Column('user_node', String(50))
    project_id = db.Column('project_id', String(50))
    project_node = db.Column('project_node', String(50))
    invest_id = db.Column('invest_id', Integer, db.ForeignKey('invest.id'), primary_key=True)
    invest_node = db.Column('invest_node', String(50))

    def __repr__(self):
        return '<Invest %d in node %s>' % (self.invest_id, self.invest_node)


class InvestReward(db.Model):
    __tablename__ = 'invest_reward'

    invest = db.Column('invest', Integer, db.ForeignKey('invest.id'), primary_key=True)
    reward = db.Column('reward', Integer, db.ForeignKey('reward.id'), primary_key=True)

    def __repr__(self):
        return '<Invest(%d) - Reward(%d)>' % (self.invest, self.reward)
