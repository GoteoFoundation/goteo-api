    # -*- coding: utf-8 -*-

import time
from flask.ext.restful import fields, marshal

from goteoapi.helpers import utc_from_local, image_url, project_url, percent
from goteoapi.decorators import ratelimit, requires_auth

from goteoapi.base_resources import BaseList as Base, Response
from .projects import contribution_resource_fields
from .rewards import favourite_resource_fields

class SummaryAPI(Base):
    """Get sumarized Statistics"""

    def __init__(self):
        super(SummaryAPI, self).__init__()

    @requires_auth
    @ratelimit()
    def get(self):
        """
        Summary Stats API
        <a href="http://developers.goteo.org/doc/reports#summary">developers.goteo.org/doc/reports#summary</a>
        This resource returns statistics about the summary in Goteo.
        ---
        tags:
            - summary_reports
        definitions:
            - schema:
                id: Summary
                properties:
                    pledged:
                        type: integer
                    matchfund-amount:
                        type: integer
                    matchfundpledge-amount:
                        type: integer
                    average-donation:
                        type: number
                    users:
                        type: integer
                    projects-received:
                        type: integer
                    projects-published:
                        type: integer
                    projects-successful:
                        type: integer
                    projects-failed:
                        type: integer
                    categories:
                        type: array
                        items:
                            $ref: '#/definitions/api_reports_community_get_Category'
                    favourite-rewards:
                        type: array
                        items:
                            $ref: '#/definitions/api_reports_rewards_get_Favourite'
                    top10-collaborations:
                        type: array
                        items:
                            $ref: '#/definitions/api_reports_projects_get_ProjectContribution'
                    top10-donations:
                        type: array
                        items:
                            $ref: '#/definitions/api_reports_projects_get_ProjectContribution'

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
                    $ref: '#/definitions/api_reports_summary_get_Summary'
            400:
                description: Invalid parameters format
        """
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
            item['description-short'] = u['subtitle']
            item['video-url'] = u['media']
            item['date-published'] = utc_from_local(u['published'])
            item['image-url'] = image_url(u['image'], 'medium', False)
            item['project-url'] = project_url(u['project'])
            top10_collaborations.append(item)

        top10_donations = []
        for u in Project.donated_list(**args):
            item = marshal(u, contribution_resource_fields)
            item['description-short'] = u['subtitle']
            item['video-url'] = u['media']
            item['date-published'] = utc_from_local(u['published'])
            item['image-url'] = image_url(u['image'], 'medium', False)
            item['project-url'] = project_url(u['project'])
            top10_donations.append(item)

        users = User.total(**args)
        categorias = UserInterest.categories(**args)

        favourites = []
        for u in Reward.favourite_reward(**args):
            item = marshal(u, favourite_resource_fields)
            favourites.append(item)


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
                'categories'              : map(lambda t: {t['id']:
                                                    {'users': t['users'],
                                                     'id': t['id'],
                                                     'name': t['name'],
                                                     'percentage-users': percent(t['users'], users)}
                                                    }, categorias),
                'top10-collaborations'    : top10_collaborations,
                'top10-donations'         : top10_donations,
                'favourite-rewards'        : favourites
            },
            filters = args.items()
        )
        return res
