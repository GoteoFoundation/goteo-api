# -*- coding: utf-8 -*-

import time

from flask.ext.restful import fields, marshal
from flask.ext.sqlalchemy import sqlalchemy
from flask_restful_swagger import swagger
from sqlalchemy import and_, or_, desc

from api import db
from api.models.reward import Reward
from api.models.project import Project, ProjectCategory
from api.models.invest import Invest, InvestReward, InvestNode
from api.models.location import Location, LocationItem
from api.decorators import *

from api.base_endpoint import BaseList as Base, Response

func = sqlalchemy.func

@swagger.model
class FavouriteRewards:
    resource_fields = {
        "icon"    : fields.String,
        "name"    : fields.String,
        "description"    : fields.String,
        "svg-url"    : fields.String,
        "total"   : fields.Integer,
    }
    required = resource_fields.keys()

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
        "favorite-rewards"         : fields.List(fields.Nested(FavouriteRewards.resource_fields)),
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
        <a href="http://developers.goteo.org/doc/reports#rewards">developers.goteo.org/doc/reports#rewards</a>
        """
        res = self._get()
        return res.response()

    def _get(self):
        """Dirty work for the get() method"""
        time_start = time.time()
        # remove not used args
        args = self.parse_args(remove=('page','limit'))

        cofinanciadores = Invest.donors_total(**args);
        renuncias = Invest.total(is_refusal=True, **args);
        favorites = []
        for u in Reward.favorite_reward(**args):
            item = marshal(u, FavouriteRewards.resource_fields)
            favorites.append(item)

        res = RewardsResponse(
            starttime = time_start,
            attributes = {
                'reward-refusal'            : renuncias,
                'percentage-reward-refusal' : percent(renuncias, cofinanciadores),
                'rewards-per-amount'        : {
                    'rewards-less-than-15'    : Invest.rewards_per_amount(0, 15, **args),
                    'rewards-between-15-30'   : Invest.rewards_per_amount(15, 30, **args),
                    'rewards-between-30-100'  : Invest.rewards_per_amount(30, 100, **args),
                    'rewards-between-100-400' : Invest.rewards_per_amount(100, 400, **args),
                    'rewards-more-than-400'   : Invest.rewards_per_amount(400,  **args),
                },
                'favorite-rewards': favorites
            },
            filters = args.items()
        )
        return res
