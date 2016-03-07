# -*- coding: utf-8 -*-

import time

from flask.ext.restful import fields, marshal
from goteoapi.decorators import ratelimit, requires_auth
from goteoapi.helpers import image_url, user_url, percent

from goteoapi.base_resources import BaseList as Base, Response

category_resource_fields = {
    'id'              : fields.Integer,
    'name'            : fields.String,
    'percentage-users': fields.Float,
    'users'           : fields.Integer
}

donation_resource_fields = {
    'user'         : fields.String,
    'name'              : fields.String,
    'profile-image-url' : fields.String,
    'profile-url' : fields.String,
    'amount'       : fields.Float,
    'contributions': fields.Integer
}

collaboration_resource_fields = {
    'user'              : fields.String,
    'name'              : fields.String,
    'profile-image-url' : fields.String,
    'profile-url' : fields.String,
    'interactions'      : fields.Integer
}

class CommunityAPI(Base):
    """Get Community Statistics"""

    def __init__(self):
        super().__init__()

    @requires_auth
    @ratelimit()
    def get(self):
        """
        Community Stats API
        <a href="http://developers.goteo.org/doc/reports#community">developers.goteo.org/doc/reports#community</a>
        This resource returns statistics about the community in Goteo.
        ---
        tags:
            - community_reports
        definitions:
            - schema:
                id: Category
                properties:
                    id:
                        type: integer
                    name:
                        type: string
                    percentage-users:
                        type: number
                    users:
                        type: integer
            - schema:
                id: Donation
                properties:
                    user:
                        type: string
                    name:
                        type: string
                    profile-image-url:
                        type: string
                    profile-url:
                        type: string
                    amount:
                        type: number
                    contributions:
                        type: integer
            - schema:
                id: Collaboration
                properties:
                    user:
                        type: string
                    name:
                        type: string
                    profile-image-url:
                        type: string
                    profile-url:
                        type: string
                    interactions:
                        type: integer
            - schema:
                id: Community
                properties:
                    users:
                        type: integer
                    donors:
                        type: integer
                    percentage-donors-users:
                        type: number
                    percentage-unsubscribed-users:
                        type: number
                    donors-collaborators:
                        type: integer
                    multidonors:
                        type: integer
                    percentage-multidonor-donors:
                        type: number
                    percentage-multidonor-users:
                        type: number
                    paypal-donors:
                        type: integer
                    creditcard-donors:
                        type: integer
                    cash-donors:
                        type: integer
                    collaborators:
                        type: integer
                    average-donors:
                        type: integer
                    average-collaborators:
                        type: integer
                    creators-donors:
                        type: integer
                    creators-collaborators:
                        type: integer
                    leading-category:
                        type: integer
                    second-category:
                        type: integer
                    users-leading-category:
                        type: integer
                    users-second-category:
                        type: integer
                    percentage-users-leading-category:
                        type: number
                    percentage-users-second-category:
                        type: number
                    categories:
                        type: array
                        items:
                            $ref: '#/definitions/api_reports_community_get_Category'
                    top10-donors:
                        type: array
                        items:
                            $ref: '#/definitions/api_reports_community_get_Donation'
                    top10-multidonors:
                        type: array
                        items:
                            $ref: '#/definitions/api_reports_community_get_Donation'
                    top10-collaborators:
                        type: array
                        items:
                            $ref: '#/definitions/api_reports_community_get_Collaboration'
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
                    $ref: '#/definitions/api_reports_community_get_Community'
            400:
                description: Invalid parameters format
        """
        ret = self._get()
        return ret.response()

    def _get(self):
        """Get()'s method dirty work"""
        from goteoapi.models.invest import Invest
        from goteoapi.models.message import Message
        from goteoapi.users.models import User, UserInterest


        time_start = time.time()
        # remove not used args
        args = self.parse_args(remove=('page','limit'))

        users = User.total(**args)
        nargs = args.copy();
        nargs['unsubscribed'] = 1;
        bajas = User.total(**nargs)
        donors = Invest.donors_total(**args)
        multidonors = Invest.multidonors_total(**args)

        paypal_donors = Invest.donors_total(method=Invest.METHOD_PAYPAL, **args)
        creditcard_donors = Invest.donors_total(method=Invest.METHOD_TPV, **args)
        cash_donors = Invest.donors_total(method=Invest.METHOD_CASH, **args)
        # paypal_multidonors = Invest.multidonors_total(**dict(args, **{'method' : Invest.METHOD_PAYPAL}))

        categorias = UserInterest.categories(**args)
        users_categoria1 = categorias[0]['users'] if len(categorias) > 0 else 0
        users_categoria2 = categorias[1]['users'] if len(categorias) > 1 else 0

        top10_multidonors = []
        for u in Invest.multidonors_list(**args):
            item = marshal(u, donation_resource_fields)
            item['profile-image-url'] = image_url(u['avatar'])
            item['profile-url'] = user_url(u['id'])
            top10_multidonors.append(item)

        top10_donors = []
        for u in Invest.donors_list(**args):
            item = marshal(u, donation_resource_fields)
            item['profile-image-url'] = image_url(u['avatar'])
            item['profile-url'] = user_url(u['id'])
            top10_donors.append(item)

        top10_collaborations = []
        for u in Message.collaborators_list(**args):
            item = marshal(u, collaboration_resource_fields)
            item['profile-image-url'] = image_url(u['avatar'])
            item['profile-url'] = user_url(u['id'])
            top10_collaborations.append(item)

        res = Response(
            starttime = time_start,
            attributes = {
                'users'                             : users,
                'donors'                            : donors,
                'multidonors'                       : multidonors,
                'percentage-donors-users'           : percent(donors, users),
                'percentage-unsubscribed-users'     : percent(bajas, users),
                'percentage-multidonor-donors'      : percent(multidonors, donors),
                'percentage-multidonor-users'       : percent(multidonors, users),
                'collaborators'                     : Message.collaborators_total(**args),
                'paypal-donors'                     : paypal_donors,
                'creditcard-donors'                 : creditcard_donors,
                'cash-donors'                       : cash_donors,
                'donors-collaborators'              : Invest.donors_collaborators_total(**args),
                'average-donors'                    : Invest.average_donors(**args),
                'average-collaborators'             : Message.average_collaborators(**args),
                'creators-donors'                   : Invest.donors_creators_total(**args),
                'creators-collaborators'            : Message.collaborators_creators_total(**args),
                'categories'                        : list(map(lambda t: {t['id']:
                                                                        {'users': t['users'],
                                                                         'id': t['id'],
                                                                         'name': t['name'],
                                                                         'percentage-users': percent(t['users'], users)}
                                                                        }, categorias)),
                'leading-category'                  : categorias[0]['id'] if len(categorias) > 0 else None,
                'users-leading-category'            : users_categoria1,
                'percentage-users-leading-category' : percent(users_categoria1, users),
                'second-category'                   : categorias[1]['id'] if len(categorias) > 1 else None,
                'users-second-category'             : users_categoria2,
                'percentage-users-second-category'  : percent(users_categoria2, users),
                'top10-multidonors'                 : top10_multidonors,
                'top10-donors'                      : top10_donors,
                'top10-collaborators'               : top10_collaborations,
            },
            filters = args.items()
        )
        return res
