    # -*- coding: utf-8 -*-

import time
from flask.ext.restful import fields, marshal
from flask_restful_swagger import swagger

from goteoapi.helpers import utc_from_local, image_url, project_url, percent
from goteoapi.decorators import *

from goteoapi.base_resources import BaseList as Base, Response
from .projects import ProjectContribution
from .community import CategoryUsers
from .rewards import FavouriteRewards

@swagger.model
@swagger.nested(**{
                'categories'           : CategoryUsers.__name__,
                'top10-collaborations' : ProjectContribution.__name__,
                'top10-donations'      : ProjectContribution.__name__
                }
            )
class SummaryResponse(Response):

    resource_fields = {
        "pledged"                : fields.Integer,
        "matchfund-amount"       : fields.Integer,
        "matchfundpledge-amount" : fields.Integer,
        "average-donation"       : fields.Float,
        "users"                  : fields.Integer,
        "projects-received"      : fields.Integer,
        "projects-published"     : fields.Integer,
        "projects-successful"    : fields.Integer,
        "projects-failed"        : fields.Integer,
        "categories"             : fields.List(fields.Nested(CategoryUsers.resource_fields)),
        "favorite-rewards"       : fields.List(fields.Nested(FavouriteRewards.resource_fields)),
        "top10-collaborations"   : fields.List(fields.Nested(ProjectContribution.resource_fields)),
        "top10-donations"        : fields.List(fields.Nested(ProjectContribution.resource_fields)),
    }

    required = resource_fields.keys()


@swagger.model
class SummaryAPI(Base):
    """Get sumarized Statistics"""

    def __init__(self):
        super(SummaryAPI, self).__init__()

    @swagger.operation(
        notes='Summary report',
        responseClass=SummaryResponse.__name__,
        nickname='projects',
        parameters=Base.INPUT_FILTERS,
        responseMessages=Base.RESPONSE_MESSAGES
    )
    @requires_auth
    @ratelimit()
    def get(self):
        """Get the Projects Report
        <a href="http://developers.goteo.org/doc/reports#projects">developers.goteo.org/doc/reports#projects</a>
        """
        ret = self._get()
        return ret.response()

    def _get(self):
        """Get()'s method dirty work"""
        from goteoapi.models.project import Project
        from goteoapi.models.invest import Invest
        from goteoapi.models.reward import Reward
        from goteoapi.users.models import User, UserInterest
        from goteoapi.calls.models import Call

        time_start = time.time()
        # remove not used args
        args = self.parse_args(remove=('page','limit'))

        top10_collaborations = []
        for u in Project.collaborated_list(**args):
            item = marshal(u, ProjectContribution.resource_fields)
            item['description-short'] = u['subtitle']
            item['video-url'] = u['media']
            item['date-published'] = utc_from_local(u['published'])
            item['image-url'] = image_url(u['image'], 'big', False)
            item['project-url'] = project_url(u['project'])
            top10_collaborations.append(item)

        top10_donations = []
        for u in Project.donated_list(**args):
            item = marshal(u, ProjectContribution.resource_fields)
            item['description-short'] = u['subtitle']
            item['video-url'] = u['media']
            item['date-published'] = utc_from_local(u['published'])
            item['image-url'] = image_url(u['image'], 'big', False)
            item['project-url'] = project_url(u['project'])
            top10_donations.append(item)

        users = User.total(**args)
        categorias = UserInterest.categories(**args)

        favorites = []
        for u in Reward.favorite_reward(**args):
            item = marshal(u, FavouriteRewards.resource_fields)
            favorites.append(item)


        res = SummaryResponse(
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
                'categories'              : map(lambda t: {t.id:
                                                    {'users': t.users,
                                                     'id': t.id,
                                                     'name': t.name,
                                                     'percentage-users': percent(t.users, users)}
                                                    }, categorias),
                'top10-collaborations'    : top10_collaborations,
                'top10-donations'         : top10_donations,
                'favorite-rewards'        : favorites
            },
            filters = args.items()
        )
        return res
