# -*- coding: utf-8 -*-

from sqlalchemy import func, Integer, String, DateTime, Float, Date
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from api.helpers import image_url, utc_from_local
from sqlalchemy import asc, or_, distinct
from api.models.location import Location, LocationItem
from api.models.project import Project, ProjectCategory
from api.models.reward import Reward
from api import db
from api.decorators import cacher

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
        if 'is_refusal' in kwargs and kwargs['is_refusal'] is not None:
            filters.append(self.resign == True)
            # FIXME: No incluir status=STATUS_REVIEWING?
            filters.append(self.status.in_([self.STATUS_PENDING,
                                            self.STATUS_CHARGED,
                                            self.STATUS_PAID,
                                            self.STATUS_RETURNED]))
        if 'is_call' in kwargs and kwargs['is_call'] is not None:
            filters.append(self.call != None)
        if 'method' in kwargs and kwargs['method'] is not None:
            filters.append(self.method == kwargs['method'])
        if 'from_date' in kwargs and kwargs['from_date'] is not None:
            filters.append(self.date_invested >= kwargs['from_date'])
        if 'to_date' in kwargs and kwargs['to_date'] is not None:
            filters.append(self.date_invested <= kwargs['to_date'])
        if 'project' in kwargs and kwargs['project'] is not None:
            filters.append(self.project.in_(kwargs['project']))
        if 'node' in kwargs and kwargs['node'] is not None:
            filters.append(self.id == InvestNode.invest_id)
            filters.append(InvestNode.invest_node.in_(kwargs['node']))
        if 'category' in kwargs and kwargs['category'] is not None:
            filters.append(self.project == ProjectCategory.project)
            filters.append(ProjectCategory.category.in_(kwargs['category']))

        if 'location' in kwargs and kwargs['location'] is not None:
            filters.append(self.user == LocationItem.item)
            filters.append(LocationItem.type == 'user')
            subquery = Location.location_subquery(**kwargs['location'])
            filters.append(LocationItem.id.in_(subquery))
            # filters.append(LocationItem.locable==1)
            #

        return filters

    @hybrid_method
    @cacher
    def total(self, **kwargs):
        """Total number of invests"""
        try:
            filters = list(self.get_filters(**kwargs))
            total = db.session.query(func.count(distinct(self.id))).filter(*filters).scalar()
            if total is None:
                total = 0
            return total
        except MultipleResultsFound:
            return 0

    @hybrid_method
    @cacher
    def donors_total(self, **kwargs):
        """Total number of diferent donors"""
        try:
            filters = list(self.get_filters(**kwargs))
            total = db.session.query(func.count(distinct(self.user))).filter(*filters).scalar()
            if total is None:
                total = 0
            return total
        except MultipleResultsFound:
            return 0

    @hybrid_method
    @cacher
    def multidonors_total(self, **kwargs):
        """Total number of donors who donates to more than 1 project"""
        filters = list(self.get_filters(**kwargs))
        filters.append(Invest.status.in_([Invest.STATUS_PENDING,
                                          Invest.STATUS_CHARGED,
                                          Invest.STATUS_PAID,
                                          Invest.STATUS_RETURNED]))
        total = db.session.query(Invest.user).filter(*filters).group_by(Invest.user).\
                                                    having(func.count(Invest.user) > 1).\
                                                    having(func.count(Invest.project) > 1)
        res = total.count()
        if res is None:
            res = 0
        return res

    @hybrid_method
    @cacher
    def pledged_total(self, **kwargs):
        """Total amount of money (€) raised by Goteo"""
        try:
            filters = list(self.get_filters(**kwargs))
            filters.append(self.project == Project.id)
            filters.append(Project.status.in_(Project.PUBLISHED_PROJECTS))
            filters.append(self.status.in_([self.STATUS_PENDING,
                                            self.STATUS_CHARGED,
                                            self.STATUS_PAID,
                                            self.STATUS_RETURNED]))
            total = db.session.query(func.sum(self.amount)).filter(*filters).scalar()
            if total is None:
                total = 0
            return total
        except MultipleResultsFound:
            return 0

    @hybrid_method
    @cacher
    def refunded_total(self, **kwargs):
        """Refunded money (€) on failed projects """
        try:
            filters = list(self.get_filters(**kwargs))
            filters.append(self.project == Project.id)
            filters.append(Project.status.in_(Project.PUBLISHED_PROJECTS))
            filters.append(self.status == self.STATUS_RETURNED)
            total = db.session.query(func.sum(self.amount)).filter(*filters).scalar()
            if total is None:
                total = 0
            return total
        except MultipleResultsFound:
            return 0

    @hybrid_method
    @cacher
    def fee_total(self, **kwargs):
        """Total fee collected by Goteo """
        # TODO: corregir para verificar valores de project_account.fee
        try:
            filters = list(self.get_filters(**kwargs))
            filters.append(self.project == Project.id)
            filters.append(Project.status.in_(Project.SUCCESSFUL_PROJECTS))
            filters.append(self.status.in_([self.STATUS_CHARGED,
                                            self.STATUS_PAID]))
            total = db.session.query(func.sum(self.amount)).filter(*filters).scalar()
            if total is None:
                total = 0
            total = float(total) * 0.08
            total = round(total, 2)
            return total
        except MultipleResultsFound:
            return 0


    # OJO: Como en reporting.php, no filtra por proyectos publicados
    # TODO: confirmar si hay que filtrar por Invest_node(ahora) o por project_node Se filtra
    @hybrid_method
    @cacher
    def rewards_per_amount(self, minim = 0, maxim = 0, **kwargs):
        """Num. of users choosing rewards from {minim} € to {maxim} € """
        filters = list(self.get_filters(**kwargs))
        # filters.append(Reward.id != None)
        filters.append(InvestReward.invest == self.id)
        filters.append(InvestReward.reward == Reward.id)
        filters.append(or_(self.resign == None, self.resign == 0))

        if minim == 0 and maxim > 0:
            filters.append(Reward.amount < maxim)
        elif minim > 0 and maxim > 0:
            filters.append(Reward.amount.between(minim, maxim))
        elif  minim > 0:
            filters.append(Reward.amount > minim)
        else:
            return 0

        recomp_dinero = db.session.query(func.count(self.id).label("amourew"))\
                            .filter(*filters).group_by(Reward.id).subquery()
        res = db.session.query(func.sum(recomp_dinero.c.amourew)).scalar()
        if res is None:
            res = 0
        return res

    @hybrid_method
    @cacher
    def percent_pledged_successful(self, **kwargs):
        """Percentage of money raised over the minimum on successful projects"""
        print '>>>>'
        filters = list(self.get_filters(**kwargs))
        filters.append(self.project == Project.id)
        filters.append(self.status.in_([self.STATUS_CHARGED,
                                        self.STATUS_PAID]))
        filters.append(Project.status.in_([Project.STATUS_FUNDED,
                                           Project.STATUS_FULFILLED]))
        sub = db.session.query((func.sum(self.amount) / Project.minimum * 100 - 100).label('percent'))\
                            .filter(*filters).group_by(self.project).subquery()
        total = db.session.query(func.avg(sub.c.percent)).scalar()
        total = 0 if total is None else round(total, 2)
        return total

    @hybrid_method
    @cacher
    def percent_pledged_failed(self, **kwargs):
        """Percentage of money raised over the minimum on failed projects """
        filters = list(self.get_filters(**kwargs))
        filters.append(self.project == Project.id)
        filters.append(self.status.in_([self.STATUS_PENDING,
                                        self.STATUS_RETURNED]))
        filters.append(Project.status == Project.STATUS_UNFUNDED)
        sub = db.session.query((func.sum(self.amount) / Project.minimum * 100).label('percent'))\
                            .filter(*filters).group_by(self.project).subquery()
        total = db.session.query(func.avg(sub.c.percent)).scalar()
        total = 0 if total is None else round(total, 2)
        return total

    @hybrid_method
    @cacher
    def average_donation(self, **kwargs):
        """Average amount of money (€) given by a donor """
        filters = list(self.get_filters(**kwargs))
        filters.append(self.project == Project.id)
        filters.append(Project.status.in_(Project.PUBLISHED_PROJECTS))
        filters.append(self.status > self.STATUS_PENDING)
        sub = db.session.query(func.avg(self.amount).label('amount')).join(Project)\
                                .filter(*filters).group_by(self.user).subquery()
        total = db.session.query(func.avg(sub.c.amount)).scalar()
        total = 0 if total is None else round(total, 2)
        return total

    @hybrid_method
    @cacher
    def average_second_round(self, **kwargs):
        """Average money raised (€) for successful projects (those which reached the minimum) """
        filters = list(self.get_filters(**kwargs))
        filters.append(self.date_invested >= Project.date_passed)
        sub = db.session.query(func.sum(self.amount).label('amount')).join(Project)\
                                            .filter(*filters).group_by(Project.id).subquery()
        total = db.session.query(func.avg(sub.c.amount)).scalar()
        total = 0 if total is None else round(total, 2)
        return total

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
