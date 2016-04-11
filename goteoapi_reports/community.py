# -*- coding: utf-8 -*-

import time

from flask.ext.restful import fields, marshal
from flasgger.utils import swag_from
from goteoapi.ratelimit import ratelimit
from goteoapi.auth.decorators import requires_auth
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

    @requires_auth()
    @ratelimit()
    @swag_from('swagger_specs/community.yml')
    def get(self):
        ret = self._get()
        return ret.response()

    def _get(self):
        """Get()'s method dirty work"""
        from goteoapi.invests.models import Invest
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
        users_categoria1 = categorias[0].users if len(categorias) > 0 else 0
        users_categoria2 = categorias[1].users if len(categorias) > 1 else 0

        top10_multidonors = []
        for u in Invest.multidonors_list(**args):
            item = marshal(u._asdict(), donation_resource_fields)
            item['profile-image-url'] = image_url(u.avatar)
            item['profile-url'] = user_url(u.id)
            top10_multidonors.append(item)

        top10_donors = []
        for u in Invest.donors_list(**args):
            item = marshal(u._asdict(), donation_resource_fields)
            item['profile-image-url'] = image_url(u.avatar)
            item['profile-url'] = user_url(u.id)
            top10_donors.append(item)

        top10_collaborations = []
        for u in Message.collaborators_list(**args):
            item = marshal(u._asdict(), collaboration_resource_fields)
            item['profile-image-url'] = image_url(u.avatar)
            item['profile-url'] = user_url(u.id)
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
                'categories'                        : list(map(lambda t: {t.id:
                                                                        {'users': t.users,
                                                                         'id': t.id,
                                                                         'name': t.name,
                                                                         'percentage-users': percent(t.users, users)}
                                                                        }, categorias)),
                'leading-category'                  : categorias[0].id if len(categorias) > 0 else None,
                'users-leading-category'            : users_categoria1,
                'percentage-users-leading-category' : percent(users_categoria1, users),
                'second-category'                   : categorias[1].id if len(categorias) > 1 else None,
                'users-second-category'             : users_categoria2,
                'percentage-users-second-category'  : percent(users_categoria2, users),
                'top10-multidonors'                 : top10_multidonors,
                'top10-donors'                      : top10_donors,
                'top10-collaborators'               : top10_collaborations,
            },
            filters = args.items()
        )
        return res
