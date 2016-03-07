# -*- coding: utf-8 -*-

import time

from flask.ext.restful import fields, marshal

from goteoapi.decorators import ratelimit, requires_auth
from goteoapi.helpers import percent
from goteoapi.base_resources import BaseList as Base, Response

favorite_resource_fields = {
    "icon"    : fields.String,
    "name"    : fields.String,
    "description"    : fields.String,
    "svg-url"    : fields.String,
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

    @requires_auth
    @ratelimit()
    def get(self):
        """
        Reward Stats API
        <a href="http://developers.goteo.org/doc/reports#rewards">developers.goteo.org/doc/reports#rewards</a>
        This resource returns statistics about rewards in Goteo.
        ---
        tags:
            - reward_reports
        definitions:
            - schema:
                id: Favourite
                properties:
                    icon:
                        type: string
                    name:
                        type: string
                    description:
                        type: string
                    svg-url:
                        type: string
                    total:
                        type: integer
            - schema:
                id: PerAmount
                properties:
                    rewards-less-than-15:
                        type: integer
                    rewards-between-15-30:
                        type: integer
                    rewards-between-30-100:
                        type: integer
                    rewards-between-100-400:
                        type: integer
                    rewards-more-than-400:
                        type: integer
            - schema:
                id: Reward
                properties:
                    reward-refusal:
                        type: integer
                    favorite-rewards:
                        type: array
                        items:
                            $ref: '#/definitions/api_reports_rewards_get_Favourite'
                    percentage-reward-refusal:
                        type: float
                    rewards-per-amount:
                        $ref: '#/definitions/api_reports_rewards_get_PerAmount'

        parameters:
            - in: query
              type: string
              name: node
              description: Filter by individual node(s). Multiple nodes can be specified
              collectionFormat: multi
            - in: query
              name: project
              description: Filter by individual project(s). Multiple projects can be specified
              type: string
              collectionFormat: multi
            - in: query
              name: from_date
              description: Filter from date. Ex. "2013-01-01"
              type: string
              format: date
            - in: query
              name: to_date
              description: Filter until date.. Ex. "2014-01-01"
              type: string
              format: date
            - in: query
              name: category
              description: Filter by project category. Multiple projects can be specified
              type: integer
            - in: query
              name: location
              description: Filter by project location (Latitude,longitude,Radius in Km)
              type: number
              collectionFormat: csv
            - in: query
              name: page
              description: Page number (starting at 1) if the result can be paginated
              type: integer
            - in: query
              name: limit
              description: Page limit (maximum 50 results, defaults to 10) if the result can be paginated
              type: integer
        responses:
            200:
                description: List of available projects
                schema:
                    $ref: '#/definitions/api_reports_rewards_get_Reward'
            400:
                description: Invalid parameters format
        """
        res = self._get()
        return res.response()

    def _get(self):
        """Dirty work for the get() method"""
        from goteoapi.models.reward import Reward
        from goteoapi.models.invest import Invest

        time_start = time.time()
        # remove not used args
        args = self.parse_args(remove=('page','limit'))

        cofinanciadores = Invest.donors_total(**args);
        renuncias = Invest.total(is_refusal=True, **args);
        favorites = []
        for u in Reward.favorite_reward(**args):
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
