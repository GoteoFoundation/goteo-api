    # -*- coding: utf-8 -*-

import time
from flask.ext.restful import marshal
from flasgger.utils import swag_from
from goteoapi.helpers import utc_from_local, image_url, project_url, percent
from goteoapi.ratelimit import ratelimit
from goteoapi.auth.decorators import requires_auth

from goteoapi.base_resources import BaseList as Base, Response
from .projects import contribution_resource_fields
from .rewards import favorite_resource_fields

class SummaryAPI(Base):
    """Get sumarized Statistics"""

    def __init__(self):
        super().__init__()

    @requires_auth()
    @ratelimit()
    @swag_from('swagger_specs/summary.yml')
    def get(self):
        ret = self._get()
        return ret.response()

    def _get(self):
        """Get()'s method dirty work"""
        from goteoapi.models.invest import Invest
        from goteoapi.models.reward import Reward
        from goteoapi.projects.models import Project
        from goteoapi.users.models import User, UserInterest
        from goteoapi.calls.models import Call

        time_start = time.time()
        # remove not used args
        args = self.parse_args(remove=('page','limit'))

        top10_collaborations = []
        for u in Project.collaborated_list(**args):
            item = marshal(u, contribution_resource_fields)
            item['description-short'] = u.subtitle
            item['video-url'] = u.media
            item['date-published'] = utc_from_local(u.published)
            item['image-url'] = image_url(u.image, 'medium', False)
            item['project-url'] = project_url(u.id)
            top10_collaborations.append(item)

        top10_donations = []
        for u in Project.donated_list(**args):
            item = marshal(u, contribution_resource_fields)
            item['description-short'] = u.subtitle
            item['video-url'] = u.media
            item['date-published'] = utc_from_local(u.published)
            item['image-url'] = image_url(u.image, 'medium', False)
            item['project-url'] = project_url(u.id)
            top10_donations.append(item)

        users = User.total(**args)
        categorias = UserInterest.categories(**args)

        favorites = []
        for u in Reward.favorite_reward(**args):
            item = marshal(u, favorite_resource_fields)
            favorites.append(item)


        res = Response(
            starttime = time_start,
            attributes = {
                'pledged'                 : Invest.pledged_total(**args),
                'matchfund-amount'        : Invest.pledged_total(method=Invest.METHOD_DROP, **args),
                'matchfundpledge-amount'  : Call.pledged_total(**args),
                'average-donation'        : Invest.average_donation(**args),
                'users'                   : users,
                'projects-received'       : Project.total(received=True, **args),
                'projects-published'      : Project.total(**args),
                'projects-successful'     : Project.total(successful=True, **args),
                'projects-failed'         : Project.total(failed=True, **args),
                'categories'              : list(map(lambda t: {t.id:
                                                    {'users': t.users,
                                                     'id': t.id,
                                                     'name': t.name,
                                                     'percentage-users': percent(t.users, users)}
                                                    }, categorias)),
                'top10-collaborations'    : top10_collaborations,
                'top10-donations'         : top10_donations,
                'favorite-rewards'       : favorites
            },
            filters = args.items()
        )
        return res
