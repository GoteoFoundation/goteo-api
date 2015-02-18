# -*- coding: utf-8 -*-

import time

from flask.ext.restful import fields
from flask.ext.sqlalchemy import sqlalchemy
from flask_restful_swagger import swagger
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import and_, or_, desc

from config import config
from api import db
from api.models.category import Category
from api.models.reward import Reward
from api.models.project import Project, ProjectCategory
from api.models.invest import Invest, InvestReward, InvestNode
from api.models.location import Location, LocationItem
from api.decorators import *

from api.base_endpoint import BaseList as Base, Response


# DEBUG
if config.debug:
    db.session.query = debug_time(db.session.query)

func = sqlalchemy.func

@swagger.model
class RewardsPerAmount:
    resource_fields = {
        "rewards-less-than-15"    : fields.Integer,
        "rewards-between-15-30"   : fields.Integer,
        "rewards-between-30-100"  : fields.Integer,
        "rewards-between-100-400" : fields.Integer,
        "rewards-more-than-400"   : fields.Integer
    }
    required = resource_fields.keys()

@swagger.model
@swagger.nested(**{"rewards-per-amount" : RewardsPerAmount.__name__})
class RewardsResponse(Response):

    resource_fields = {
        "reward-refusal"           : fields.Integer,
        "favorite-rewards"         : fields.List,
        "percentage-reward-refusal": fields.Float,
        "rewards-per-amount"       : fields.Nested(RewardsPerAmount.resource_fields)
    }

    required = resource_fields.keys()


@swagger.model
class RewardsAPI(Base):
    """Get Rewards Statistics"""

    def __init__(self):
        super(RewardsAPI, self).__init__()

    @swagger.operation(
        notes='Rewards report',
        responseClass=RewardsResponse.__name__,
        nickname='rewards',
        parameters=Base.INPUT_FILTERS,
        responseMessages=Base.RESPONSE_MESSAGES
    )
    @requires_auth
    @ratelimit()
    def get(self):
        """Get the Rewards Report
        <a href="http://developers.goteo.org/reports#rewards">developers.goteo.org/reports#rewards</a>
        """
        time_start = time.time()
        self.reqparse.remove_argument('page')
        self.reqparse.remove_argument('limit')
        args = self.reqparse.parse_args()

        filters = []
        filters2 = []  # para favorite_reward
        # TODO: Qué fechas coger? creacion, finalizacion?
        if args['from_date']:
            filters.append(Invest.date_invested >= args['from_date'])
            filters2.append(Invest.date_invested >= args['from_date'])
            filters2.append(Invest.project == Project.id)
        if args['to_date']:
            filters.append(Invest.date_invested <= args['to_date'])
            filters2.append(Invest.date_invested <= args['to_date'])
            filters2.append(Invest.project == Project.id)
        if args['project']:
            filters.append(Invest.project.in_(args['project'][0]))
            filters2.append(Invest.project.in_(args['project'][0]))
            filters2.append(Invest.project == Project.id)
        if args['node']:
            # FIXME: invest_node o project_node ?
            filters.append(Invest.id == InvestNode.invest_id)
            filters2.append(Project.id == InvestNode.project_id)
            filters.append(InvestNode.project_node.in_(args['node']))
            filters2.append(InvestNode.project_node.in_(args['node']))
        if args['category']:
            filters.append(Invest.project == ProjectCategory.project)
            filters2.append(Project.id == ProjectCategory.project)
            filters.append(ProjectCategory.category.in_(args['category']))
            filters2.append(ProjectCategory.category.in_(args['category']))
        if args['location']:
            # Filtra por la localización del usuario que elige la recompensa
            # No hace falta filters2, ya que ese filtra por proyecto, no por usuario

            locations_ids = Location.location_ids(**args['location'])

            if locations_ids == []:
                return bad_request("No locations in the specified range")

            filters.append(Invest.user == LocationItem.item)
            filters.append(LocationItem.type == 'user')
            filters.append(LocationItem.id.in_(locations_ids))

        cofinanciadores = self._cofinanciadores(list(filters));
        renuncias = self._renuncias(list(filters));
        res = RewardsResponse(
            starttime = time_start,
            attributes = {
                'reward-refusal'            : renuncias,
                'percentage-reward-refusal' : percent(renuncias, cofinanciadores),
                'rewards-per-amount'        : {
                    'rewards-less-than-15'    : self._recomp_dinero(list(filters), 0, 15),
                    'rewards-between-15-30'   : self._recomp_dinero(list(filters), 15, 30),
                    'rewards-between-30-100'  : self._recomp_dinero(list(filters), 30, 100),
                    'rewards-between-100-400' : self._recomp_dinero(list(filters), 100, 400),
                    'rewards-more-than-400'   : self._recomp_dinero(list(filters), 400),
                },
                'favorite-rewards': self._favorite_reward(list(filters2))
            },
            filters = args.items()
        )
        return res.response()

    #Numero de cofinanciadores
    def _cofinanciadores(self, filters = []):
        res = db.session.query(func.count(func.distinct(Invest.user))).filter(*filters).scalar()
        if res is None:
            res = 0
        return res

    # NÚMERO de cofinanciadores que renuncian a recompensa
    # FIXME: No incluir status=STATUS_REVIEWING?
    def _renuncias(self, f_renuncias = []):
        f_renuncias.append(Invest.resign == 1)
        f_renuncias.append(Invest.status.in_([Invest.STATUS_PENDING,
                                              Invest.STATUS_CHARGED,
                                              Invest.STATUS_PAID,
                                              Invest.STATUS_RETURNED]))
        res = db.session.query(func.count(Invest.id)).filter(*f_renuncias).scalar()
        if res is None:
            res = 0
        return res

    # Recompensas elegindas para valores minimos y máximos
    # OJO: Como en reporting.php, no filtra por proyectos publicados
    def _recomp_dinero(self, f_recomp_dinero = [], minim = 0, maxim = 0):
        f_recomp_dinero.append(Reward.id != None)
        f_recomp_dinero.append(or_(Invest.resign == None, Invest.resign == 0))

        if minim == 0 and maxim > 0:
            f_recomp_dinero.append(Reward.amount < maxim)
        elif minim > 0 and maxim > 0:
            f_recomp_dinero.append(Reward.amount.between(minim, maxim))
        elif  minim > 0:
            f_recomp_dinero.append(Reward.amount > minim)
        else:
            return 0

        recomp_dinero = db.session.query(func.count(Invest.id).label("amourew")).join(InvestReward).join(Reward)\
                            .filter(*f_recomp_dinero).group_by(Reward.id).subquery()
        res = db.session.query(func.sum(recomp_dinero.c.amourew)).scalar()
        if res is None:
            res = 0
        return res


    # Tipo de recompensa más utilizada en proyectos exitosos
    # FIXME: Date: Project.published
    def _favorite_reward(self, f_favorite_reward = []):
        f_favorite_reward.append(Reward.type == 'individual')
        res = db.session.query(Reward.icon, func.count(Reward.project).label('total'))\
                                .join(Project, and_(Project.id == Reward.project, Project.status.in_([
                                    Project.STATUS_IN_CAMPAIGN,
                                    Project.STATUS_FUNDED,
                                    Project.STATUS_FULLFILED])))\
                                .filter(*f_favorite_reward).group_by(Reward.icon).order_by(desc('total')).all()
        if res is None:
            res = []
        return res
