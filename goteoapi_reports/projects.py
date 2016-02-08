    # -*- coding: utf-8 -*-

import time
from flask.ext.restful import fields, marshal

from goteoapi.decorators import ratelimit, requires_auth
from goteoapi.helpers import utc_from_local, image_url, project_url, percent
from goteoapi.base_resources import BaseList as Base, Response

contribution_resource_fields = {
    'project'  : fields.String,
    'name'  : fields.String,
    'project-url'  : fields.String,
    'description-short'  : fields.String,
    'image-url'  : fields.String,
    'video-url'  : fields.String,
    'date-published'  : fields.DateTime(dt_format='rfc822'),
    'total' : fields.Integer
}

amount_resource_fields = {
    'project'   : fields.String,
    'name'   : fields.String,
    'project-url'   : fields.String,
    'description-short'  : fields.String,
    'image-url'  : fields.String,
    'video-url'  : fields.String,
    'date-published'  : fields.DateTime(dt_format='rfc822'),
    'amount' : fields.Float
}

class ProjectsAPI(Base):
    """Projects Statistics"""

    def __init__(self):
        super(ProjectsAPI, self).__init__()

    @requires_auth
    @ratelimit()
    def get(self):
        """
        Projects Stats API
        <a href="http://developers.goteo.org/doc/reports#projects">developers.goteo.org/doc/reports#projects</a>
        This resource returns statistics about projects in Goteo.
        ---
        tags:
            - project_reports
        definitions:
            - schema:
                id: ProjectContribution
                properties:
                    project:
                        type: string
                    name:
                        type: string
                    project-url:
                        type: string
                    description-short:
                        type: string
                    image-url:
                        type: string
                    video-url:
                        type: string
                    date-published:
                        type: string
                    total:
                        type: integer
            - schema:
                id: ProjectAmount
                properties:
                    project:
                        type: string
                    name:
                        type: string
                    project-url:
                        type: string
                    description-short:
                        type: string
                    image-url:
                        type: string
                    video-url:
                        type: string
                    date-published:
                        type: string
                    total:
                        type: integer
            - schema:
                id: Project
                properties:
                    failed:
                        type: integer
                    published:
                        type: integer
                    received:
                        type: integer
                    successful:
                        type: integer
                    successful:
                        type: integer
                    percentage:
                        type: number
                    percentage:
                        type: number
                    average-amount:
                        type: number
                    top10-collaborations:
                        type: array
                        items:
                            $ref: '#/definitions/api_reports_projects_get_ProjectContribution'
                    top10-donations:
                        type: array
                        items:
                            $ref: '#/definitions/api_reports_projects_get_ProjectContribution'
                    top10-receipts:
                        type: array
                        items:
                            $ref: '#/definitions/api_reports_projects_get_ProjectAmount'
                    average-posts:
                        type: number
        parameters:
            - in: query
              type: string
              name: node
              description: Filter by individual node(s). Multiple nodes can be specified.
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
                    $ref: '#/definitions/api_reports_projects_get_Project'
            400:
                description: Invalid parameters format
        """
        ret = self._get()
        return ret.response()

    def _get(self):
        """Get()'s method dirty work"""
        from goteoapi.projects.models import Project

        time_start = time.time()
        # remove not used args
        args = self.parse_args(remove=('page','limit'))

        succ_projects = Project.total(successful=True, **args)
        # succ_projects_closed = Project.total(closed=True, **args)
        succ_finished = Project.total(finished=True, **args)
        fail_projects = Project.total(failed=True, **args)

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

        top10_receipts = []
        for u in Project.received_list(finished=True, **args):
            item = marshal(u, amount_resource_fields)
            item['description-short'] = u['subtitle']
            item['video-url'] = u['media']
            item['date-published'] = utc_from_local(u['published'])
            item['image-url'] = image_url(u['image'], 'medium', False)
            item['project-url'] = project_url(u['project'])
            top10_receipts.append(item)

        res = Response(
            starttime = time_start,
            attributes = {
                'received'                       : Project.total(received=True, **args),
                'published'                      : Project.total(**args),
                'failed'                         : fail_projects,
                'successful'                     : succ_projects,
                'successful-completed'           : succ_finished,
                'percentage-successful'          : percent(succ_projects, succ_projects + fail_projects),
                'percentage-successful-completed': percent(succ_finished, succ_finished + fail_projects),
                'average-amount-successful'      : Project.average_total(successful=True, **args),
                'average-posts-successful'       : Project.average_posts(successful=True, **args),
                'top10-collaborations'           : top10_collaborations,
                'top10-donations'                : top10_donations,
                'top10-receipts'                 : top10_receipts,
            },
            filters = args.items()
        )
        return res
