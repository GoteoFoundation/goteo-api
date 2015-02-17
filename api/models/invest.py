# -*- coding: utf-8 -*-

from sqlalchemy import func, Integer, String, DateTime, Float, Date
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from api.helpers import image_url, utc_from_local
from sqlalchemy import asc
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
