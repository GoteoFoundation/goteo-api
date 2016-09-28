# -*- coding: utf-8 -*-

from sqlalchemy import func, desc, Integer, String, Date, Boolean, Float
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from sqlalchemy import or_, not_, and_, distinct

from ..cacher import cacher

from ..projects.models import Project, ProjectCategory
from ..location.models import InvestLocation
from ..models.reward import Reward
from ..models.message import Message
from ..helpers import utc_from_local
from .. import db


class Invest(db.Model):
    __tablename__ = 'invest'

    METHOD_PAYPAL = 'paypal'
    METHOD_TPV = 'tpv'
    METHOD_CASH = 'cash'
    METHOD_DROP = 'drop'

    # INVEST STATUS IDs
    # payment gateway not reached yet or just a failed payment
    STATUS_PROCESSING = -1
    # In a status that requires post-processing (former paypal preapprovals)
    STATUS_PENDING = 0
    # charged by the platform
    STATUS_CHARGED = 1
    # refunded to the user by some admin manual action,
    # won't be added to any total
    STATUS_CANCELLED = 2
    # paid to the project (successful project) NOT REALLY USED
    STATUS_PAID = 3
    # automatically refunded to the user due a failed project
    STATUS_RETURNED = 4
    # deprecated status
    STATUS_RELOCATED = 5
    # refunded to user's pool
    STATUS_TO_POOL = 6

    VALID_INVESTS = [STATUS_PENDING,
                     STATUS_CHARGED,
                     STATUS_PAID,
                     STATUS_RETURNED,
                     STATUS_TO_POOL]
    NON_FISICAL_INVESTS = ('drop', 'pool')
    STATUS_STR = ('processing',
                  'pending',
                  'charged',
                  'cancelled',
                  'paid',
                  'returned',
                  'relocated',
                  'pool-returned')

    id = db.Column('id', Integer, primary_key=True)
    user_id = db.Column('user', String(50), db.ForeignKey('user.id'))
    project_id = db.Column('project', String(50), db.ForeignKey('project.id'))
    call_id = db.Column('call', String(50), db.ForeignKey('call.id'))
    status = db.Column('status', Integer)
    amount = db.Column('amount', Integer)
    method = db.Column('method', String(20))
    currency = db.Column('currency', String(3))
    conversion_ratio = db.Column('currency_rate', Float)
    anonymous = db.Column('anonymous', Boolean, nullable=False)
    created = db.Column('invested', Date)
    charged = db.Column('charged', Date)
    updated = db.Column('datetime', Date)
    returned = db.Column('returned', Date)
    resign = db.Column('resign', Boolean, nullable=False)
    # True if the invest goes to pool in case of failing
    pool = db.Column('pool', Boolean, nullable=False)

    def __repr__(self):
        return '<Invest %d: %s (%d EUR)>' % (
            self.id, self.project_id, self.amount)

    @hybrid_property
    def user(self):
        from ..users.models import User
        return User.get(self.user_id)

    @hybrid_property
    def owner(self):
        if(self.anonymous):
            return None
        return self.user_id

    @hybrid_property
    def owner_name(self):
        if(self.anonymous):
            return 'Anonymous'
        return self.user.name

    @hybrid_property
    def date_created(self):
        return utc_from_local(self.created)

    @hybrid_property
    def date_charged(self):
        return utc_from_local(self.charged)

    @hybrid_property
    def date_returned(self):
        return utc_from_local(self.returned)

    @hybrid_property
    def date_updated(self):
        return utc_from_local(self.updated)

    @hybrid_property
    def status_string(self):
        return self.STATUS_STR[self.status + 1]

    @hybrid_property
    def type(self):
        if self.method in self.NON_FISICAL_INVESTS:
            return self.method
        return 'payment'

    # Getting filters for this model
    @hybrid_method
    def get_filters(self, **kwargs):

        filters = []

        if 'status' in kwargs and kwargs['status'] is not None:
            if isinstance(kwargs['status'], (list, tuple)):
                filters.append(self.status.in_(kwargs['status']))
            else:
                filters.append(self.status == kwargs['status'])
        else:
            filters.append(self.status.in_(self.VALID_INVESTS))

        #  is_refusal == False   => Invests without reward
        #  is_refusal == True   => Invests with reward
        #  is_refusal == None  => all Invests
        if 'is_refusal' in kwargs and kwargs['is_refusal'] is not None:
            if kwargs['is_refusal'] is True:
                filters.append(self.resign == True)
            elif kwargs['is_refusal'] is False:
                filters.append(or_(self.resign == None, self.resign == False))
        #  is_anonymous == False   => Not anonymous Invests
        #  is_anonymous == True   => Anonymous Invests
        #  is_anonymous == None  => all Invests
        if 'is_anonymous' in kwargs and kwargs['is_anonymous'] is not None:
            if kwargs['is_anonymous'] is True:
                filters.append(self.anonymous == True)
            elif kwargs['is_anonymous'] is False:
                filters.append(or_(self.anonymous == None,
                                   self.anonymous == False))

        # Search by user
        if 'user' in kwargs and kwargs['user'] is not None:
            if isinstance(kwargs['user'], (list, tuple)):
                filters.append(self.user_id.in_(kwargs['user']))
            else:
                filters.append(self.user_id == kwargs['user'])

        # Can be used to get Invest applying to a Call
        # or Invests not applying to any Call if None
        #  call == False   => Invest not applying to any Call
        #  call == True   => Invest applying to any Call
        #  call == 'call-id'   => Invest applying to that specific Call
        if 'call' in kwargs and kwargs['call'] is not None:
            if kwargs['call'] is True:
                filters.append(and_(self.call_id != None,
                                    self.call_id != ''))
            elif kwargs['call'] is False:
                filters.append(or_(self.call_id == None, self.call_id == ''))
            else:
                if isinstance(kwargs['call'], (list, tuple)):
                    filters.append(self.call_id.in_(kwargs['call']))
                else:
                    filters.append(self.call_id == kwargs['call'])

        # Can be used to get Invest applying to a Project
        # or Invests not applying to any Project if None
        #  project == False  => Invest not applying to any Project
        #  project == True  => Invest applying to any Project
        #  project == 'project-id'  => Invest applying to that specific Project
        if 'project' in kwargs and kwargs['project'] is not None:
            if kwargs['project'] is True:
                filters.append(and_(self.project_id != None,
                                    self.project_id != ''))
            elif kwargs['project'] is False:
                filters.append(or_(self.project_id != None,
                                   self.project_id == ''))
            else:
                if isinstance(kwargs['project'], (list, tuple)):
                    filters.append(self.project_id.in_(kwargs['project']))
                else:
                    filters.append(self.project_id == kwargs['project'])

        # instead of exposing raw payment method
        # we will show 3 main methods as 'type' property:
        # - drop (comming from matchunding call)
        # - pool (comming from virtual wallet)
        # - payment (fisical payment)
        if 'type' in kwargs:
            if kwargs['type'] in self.NON_FISICAL_INVESTS:
                filters.append(self.method == kwargs['type'])
            if kwargs['type'] == 'payment':
                filters.append(not_(self.method.in_(self.NON_FISICAL_INVESTS)))

        if 'method' in kwargs and kwargs['method'] is not None:
            filters.append(self.method == kwargs['method'])

        if 'not_method' in kwargs and kwargs['not_method'] is not None:
            filters.append(self.method != kwargs['not_method'])

        if 'from_date' in kwargs and kwargs['from_date'] is not None:
            filters.append(self.created >= kwargs['from_date'])

        if 'to_date' in kwargs and kwargs['to_date'] is not None:
            filters.append(self.created <= kwargs['to_date'])

        if 'node' in kwargs and kwargs['node'] is not None:
            filters.append(self.id == InvestNode.invest_id)
            filters.append(InvestNode.invest_node.in_(kwargs['node']))

        if 'category' in kwargs and kwargs['category'] is not None:
            filters.append(self.project_id == ProjectCategory.project_id)
            filters.append(ProjectCategory.category_id.in_(kwargs['category']))

        if 'location' in kwargs and kwargs['location'] is not None:
            filters.append(self.id == InvestLocation.id)
            subquery = InvestLocation.location_subquery(**kwargs['location'])
            filters.append(InvestLocation.id.in_(subquery))

        if 'loc_status' in kwargs and kwargs['loc_status'] is not None:
            if kwargs['loc_status'] == 'located':
                filters.append(self.id.in_(
                    db.session.query(InvestLocation.id).subquery()))
            if kwargs['loc_status'] == 'unlocated':
                filters.append(~self.id.in_(
                    db.session.query(InvestLocation.id).subquery()))

        return filters

    @hybrid_method
    @cacher
    def get(self, invest_id):
        """Get a valid invest form id"""
        try:
            filters = self.get_filters()
            filters.append(self.id == invest_id)
            return self.query.filter(*filters).one()
        except NoResultFound:
            return None

    @hybrid_method
    @cacher
    def total(self, **kwargs):
        """Total number of invests"""
        try:
            filters = list(self.get_filters(**kwargs))
            total = db.session.query(func.count(distinct(self.id))) \
                              .filter(*filters).scalar()
            if total is None:
                total = 0
            return total
        except MultipleResultsFound:
            return 0

    @hybrid_method
    @cacher
    def list(self, **kwargs):
        """Get a list of valid invests"""
        try:
            limit = kwargs['limit'] if 'limit' in kwargs else 10
            page = kwargs['page'] if 'page' in kwargs else 0
            filters = self.get_filters(**kwargs)
            return self.query.distinct().filter(*filters) \
                                        .order_by(desc(self.id)) \
                                        .offset(page * limit) \
                                        .limit(limit).all()
        except NoResultFound:
            return []

    # Top 10 Cofinanciadores con más caudal (más generosos)
    # excluir usuarios convocadores Y ADMINES
    @hybrid_method
    @cacher
    def donors_list(self, **kwargs):
        """List of donors"""
        from ..users.models import User, UserRole
        from ..calls.models import Call

        limit = kwargs['limit'] if 'limit' in kwargs else 10
        page = kwargs['page'] if 'page' in kwargs else 0
        filters = list(self.get_filters(**kwargs))
        filters.append(self.status.in_(self.VALID_INVESTS))
        filters.append(self.user_id == User.id)
        # exclude convocadores, admines y owners
        admins = db.session.query(UserRole.user_id) \
                   .filter(UserRole.role_id == 'superadmin') \
                   .subquery()
        calls = db.session.query(Call.user_id) \
                  .filter(Call.status > Call.STATUS_REVIEWING) \
                  .subquery()
        owners = db.session \
                   .query(Project.user_id) \
                   .filter(Project.status.in_(Project.PUBLISHED_PROJECTS)) \
                   .subquery()
        filters.append(~self.user_id.in_(admins))
        filters.append(~self.user_id.in_(calls))
        filters.append(~self.user_id.in_(owners))
        try:
            return db.session.query(self.user_id,
                                    User.name,
                                    User.id,
                                    User.avatar,
                                    func.count(distinct(self.project_id))
                                        .label('contributions'),
                                    func.sum(self.amount).label('amount')) \
                             .filter(*filters).group_by(self.user_id) \
                             .order_by(desc('amount'), desc('contributions')) \
                             .offset(page * limit).limit(limit).all()
        except NoResultFound:
            return []

    @hybrid_method
    @cacher
    def multidonors_list(self, **kwargs):
        """List of multidonors"""
        from ..users.models import User, UserRole
        from ..calls.models import Call

        limit = kwargs['limit'] if 'limit' in kwargs else 10
        page = kwargs['page'] if 'page' in kwargs else 0
        filters = list(self.get_filters(**kwargs))

        filters.append(self.status.in_(self.VALID_INVESTS))
        filters.append(self.user_id == User.id)
        # exclude convocadores, admines y owners
        admins = db.session.query(UserRole.user_id) \
                   .filter(UserRole.role_id == 'superadmin') \
                   .subquery()
        calls = db.session.query(Call.user_id) \
                  .filter(Call.status > Call.STATUS_REVIEWING) \
                  .subquery()
        owners = db.session.query(Project.user_id) \
                   .filter(Project.status.in_(Project.PUBLISHED_PROJECTS)) \
                   .subquery()
        filters.append(~self.user_id.in_(admins))
        filters.append(~self.user_id.in_(calls))
        filters.append(~self.user_id.in_(owners))
        try:
            return db.session.query(self.user_id,
                                    User.name,
                                    User.id,
                                    User.avatar,
                                    func.count(distinct(self.project_id))
                                        .label('contributions'),
                                    func.sum(self.amount).label('amount')) \
                             .filter(*filters).group_by(self.user_id) \
                             .order_by(desc('contributions'), desc('amount')) \
                             .offset(page * limit).limit(limit).all()
        except NoResultFound:
            return []

    @hybrid_method
    @cacher
    def donors_total(self, **kwargs):
        """Total number of diferent donors"""
        try:
            filters = list(self.get_filters(**kwargs))
            total = db.session.query(func.count(distinct(self.user_id))) \
                      .filter(*filters).scalar()
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
        filters.append(self.status.in_(self.VALID_INVESTS))
        total = db.session.query(self.user_id) \
                          .filter(*filters) \
                          .group_by(self.user_id) \
                          .having(func.count(self.user_id) > 1) \
                          .having(func.count(self.project_id) > 1)
        res = total.count()
        if res is None:
            res = 0
        return res

    @hybrid_method
    @cacher
    def donors_collaborators_total(self, **kwargs):
        """Total number of collaborators with investions"""
        filters = list(self.get_filters(**kwargs))
        sq_blocked = db.session.query(Message.id) \
                       .filter(Message.blocked == 1).subquery()
        filters.append(Message.thread > 0)
        filters.append(Message.thread.in_(sq_blocked))
        filters.append(self.status.in_(self.VALID_INVESTS))
        res = db.session.query(func.count(func.distinct(self.user_id))) \
                        .join(Message, Message.user_id == self.user_id) \
                        .filter(*filters).scalar()
        if res is None:
            res = 0
        return res

    @hybrid_method
    @cacher
    def donors_creators_total(self, **kwargs):
        """Total number of donors who are also creators for some projects"""
        filters = list(self.get_filters(**kwargs))
        filters.append(self.status.in_([self.STATUS_PAID,
                                        self.STATUS_RETURNED,
                                        self.STATUS_RELOCATED]))
        filters.append(self.project_id != Project.id)
        res = db.session.query(func.count(func.distinct(self.user_id))) \
                .join(Project,
                      and_(Project.user_id == self.user_id,
                           Project.status.in_(Project.PUBLISHED_PROJECTS))) \
                .filter(*filters).scalar()
        if res is None:
            res = 0
        return res

    @hybrid_method
    @cacher
    def projects_total(self, **kwargs):
        """Total projects in the invest list Goteo"""
        try:
            filters = list(self.get_filters(**kwargs))
            filters.append(self.project_id == Project.id)
            filters.append(Project.status.in_(Project.PUBLISHED_PROJECTS))
            filters.append(self.status.in_(self.VALID_INVESTS))
            total = db.session \
                      .query(func.count(func.distinct(self.project_id))) \
                      .filter(*filters).scalar()
            if total is None:
                total = 0
            return total
        except MultipleResultsFound:
            return 0

    @hybrid_method
    @cacher
    def calls_total(self, **kwargs):
        """Total calls in the invest list Goteo"""
        from ..calls.models import Call
        try:
            filters = list(self.get_filters(**kwargs))
            filters.append(self.call_id == Call.id)
            filters.append(Call.status.in_(Call.PUBLIC_CALLS))
            filters.append(self.status.in_(self.VALID_INVESTS))
            total = db.session.query(func.count(func.distinct(self.call_id))) \
                      .filter(*filters).scalar()
            if total is None:
                total = 0
            return total
        except MultipleResultsFound:
            return 0

    @hybrid_method
    @cacher
    def pledged_total(self, **kwargs):
        """Total amount of money (€) raised by Goteo"""
        try:
            filters = list(self.get_filters(**kwargs))
            filters.append(self.project_id == Project.id)
            filters.append(Project.status.in_(Project.PUBLISHED_PROJECTS))
            filters.append(self.status.in_(self.VALID_INVESTS))
            total = db.session.query(func.sum(self.amount)) \
                      .filter(*filters).scalar()
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
            filters.append(self.project_id == Project.id)
            filters.append(Project.status.in_(Project.PUBLISHED_PROJECTS))
            filters.append(self.status == self.STATUS_RETURNED)
            total = db.session.query(func.sum(self.amount)) \
                      .filter(*filters).scalar()
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
            filters.append(self.project_id == Project.id)
            filters.append(Project.status.in_(Project.SUCCESSFUL_PROJECTS))
            filters.append(self.status.in_([self.STATUS_CHARGED,
                                            self.STATUS_PAID]))
            total = db.session.query(func.sum(self.amount)) \
                      .filter(*filters).scalar()
            if total is None:
                total = 0
            total = float(total) * 0.08
            total = round(total, 2)
            return total
        except MultipleResultsFound:
            return 0

    @hybrid_method
    @cacher
    def rewards_per_amount(self, minim=0, maxim=0, **kwargs):
        """Num. of users choosing rewards from {minim} € to {maxim} € """
        filters = list(self.get_filters(**kwargs))
        # filters.append(Reward.id != None)
        filters.append(InvestReward.invest_id == self.id)
        filters.append(InvestReward.reward_id == Reward.id)
        filters.append(or_(self.resign == None,
                           self.resign == False,
                           self.resign == 0))

        if minim == 0 and maxim > 0:
            filters.append(Reward.amount < maxim)
        elif minim > 0 and maxim > 0:
            filters.append(Reward.amount.between(minim, maxim))
        elif minim > 0:
            filters.append(Reward.amount > minim)
        else:
            return 0

        q_amount = db.session \
                     .query(func.count(self.id).label("amourew")) \
                     .filter(*filters) \
                     .group_by(Reward.id) \
                     .subquery()
        res = db.session.query(func.sum(q_amount.c.amourew)).scalar()
        if res is None:
            res = 0
        return res

    @hybrid_method
    @cacher
    def percent_pledged_successful(self, **kwargs):
        """Percentage of money raised over the minimum
        on successful projects
        """
        filters = list(self.get_filters(**kwargs))
        filters.append(self.project_id == Project.id)
        filters.append(self.status.in_([self.STATUS_CHARGED,
                                        self.STATUS_PAID]))
        filters.append(Project.status.in_([Project.STATUS_FUNDED,
                                           Project.STATUS_FULFILLED]))
        sub = db.session \
                .query((func.sum(self.amount) / Project.minimum * 100 - 100)
                       .label('percent')) \
                .filter(*filters) \
                .group_by(self.project_id) \
                .subquery()
        total = db.session.query(func.avg(sub.c.percent)).scalar()
        total = 0 if total is None else round(total, 2)
        return total

    @hybrid_method
    @cacher
    def percent_pledged_failed(self, **kwargs):
        """Percentage of money raised over the minimum on failed projects"""
        filters = list(self.get_filters(**kwargs))
        filters.append(self.project_id == Project.id)
        filters.append(self.status.in_([self.STATUS_PENDING,
                                        self.STATUS_RETURNED]))
        filters.append(Project.status == Project.STATUS_UNFUNDED)
        sub = db.session \
                .query((func.sum(self.amount) / Project.minimum * 100)
                       .label('percent')) \
                .filter(*filters) \
                .group_by(self.project_id) \
                .subquery()
        total = db.session.query(func.avg(sub.c.percent)).scalar()
        total = 0 if total is None else round(total, 2)
        return total

    @hybrid_method
    @cacher
    def average_donors(self, **kwargs):
        """Average number of donors"""
        filters = list(self.get_filters(**kwargs))
        filters.append(Project.status.in_([Project.STATUS_FUNDED,
                                           Project.STATUS_FULFILLED]))
        sq = db.session \
               .query(func.count(func.distinct(self.user_id)).label("co")) \
               .join(Project, self.project_id == Project.id) \
               .filter(*filters) \
               .group_by(self.project_id) \
               .subquery()
        res = db.session.query(func.avg(sq.c.co)).scalar()
        if res is None:
            res = 0
        return res

    @hybrid_method
    @cacher
    def average_donation(self, **kwargs):
        """Average amount of money (€) given by a donor"""
        filters = list(self.get_filters(**kwargs))
        filters.append(self.project_id == Project.id)
        filters.append(Project.status.in_(Project.PUBLISHED_PROJECTS))
        filters.append(self.status > self.STATUS_PENDING)
        sub = db.session.query(func.avg(self.amount).label('amount')) \
                        .join(Project) \
                        .filter(*filters) \
                        .group_by(self.user_id) \
                        .subquery()
        total = db.session.query(func.avg(sub.c.amount)).scalar()
        total = 0 if total is None else round(total, 2)
        return total

    @hybrid_method
    @cacher
    def average_second_round(self, **kwargs):
        """Average money raised (€) for successful projects
        (those which reached the minimum)
        """
        filters = list(self.get_filters(**kwargs))
        filters.append(self.created >= Project.passed)
        sub = db.session.query(func.sum(self.amount).label('amount')) \
                        .join(Project) \
                        .filter(*filters) \
                        .group_by(Project.id) \
                        .subquery()
        total = db.session.query(func.avg(sub.c.amount)).scalar()
        total = 0 if total is None else round(total, 2)
        return total


class InvestNode(db.Model):
    __tablename__ = 'invest_node'

    user_id = db.Column('user_id', String(50))
    user_node = db.Column('user_node', String(50))
    project_id = db.Column('project_id', String(50))
    project_node = db.Column('project_node', String(50))
    invest_id = db.Column('invest_id', Integer,
                          db.ForeignKey('invest.id'), primary_key=True)
    invest_node = db.Column('invest_node', String(50))

    def __repr__(self):
        return '<InvestNode %d in node %s>' % (
            self.invest_id, self.invest_node)


class InvestReward(db.Model):
    __tablename__ = 'invest_reward'

    invest_id = db.Column('invest', Integer,
                          db.ForeignKey('invest.id'), primary_key=True)
    reward_id = db.Column('reward', Integer,
                          db.ForeignKey('reward.id'), primary_key=True)

    def __repr__(self):
        return '<InvestReward(%d) - Reward(%d)>' % (self.invest, self.reward)
