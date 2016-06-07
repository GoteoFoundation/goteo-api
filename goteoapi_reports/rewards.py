# -*- coding: utf-8 -*-

import time

from flask.ext.restful import fields
from flasgger.utils import swag_from
from goteoapi.ratelimit import ratelimit
from goteoapi.auth.decorators import requires_auth
from goteoapi.helpers import percent, marshal
from goteoapi.base_resources import BaseList as Base, Response

favorite_resource_fields = {
    "icon"    : fields.String,
    "name"    : fields.String,
    "description"    : fields.String,
    "svg_url"    : fields.String,
    "total"   : fields.Integer,
}

per_amount_resource_fields = {
    "rewards-less-than-15"    : fields.Integer,
    "rewards-between-15-30"   : fields.Integer,
    "rewards-between-30-100"  : fields.Integer,
    "rewards-between-100-400" : fields.Integer,
    "rewards-more-than-400"   : fields.Integer
}


class RewardsAPI(Base):
    """Get Rewards Statistics"""

    def __init__(self):
        super().__init__()

    @requires_auth()
    @ratelimit()
    @swag_from('swagger_specs/rewards.yml')
    def get(self):
        res = self._get()
        return res.response()

    def _get(self):
        """Dirty work for the get() method"""
        # from goteoapi.models.reward import Reward
        from goteoapi.models.icon import Icon
        from goteoapi.invests.models import Invest

        time_start = time.time()
        # remove not used args
        args = self.parse_args(remove=('page','limit'))

        cofinanciadores = Invest.donors_total(**args)
        renuncias = Invest.total(is_refusal=True, **args)
        favorites = []

        for u in Icon.list(**args):
            item = marshal(u, favorite_resource_fields)
            favorites.append(item)

        res = Response(
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
