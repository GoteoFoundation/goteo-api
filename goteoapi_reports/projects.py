    # -*- coding: utf-8 -*-

import time
from flask.ext.restful import fields, marshal
from flask_restful_swagger import swagger

from goteoapi.decorators import *

from goteoapi.base_resources import BaseList as Base, Response

@swagger.model
class ProjectContribution:
    resource_fields = {
        'project'  : fields.String,
        'name'  : fields.String,
        'project-url'  : fields.String,
        'description-short'  : fields.String,
        'image-url'  : fields.String,
        'video-url'  : fields.String,
        'date-published'  : fields.DateTime(dt_format='rfc822'),
        'total' : fields.Integer
    }
    required = resource_fields.keys()

@swagger.model
class ProjectAmount:
    resource_fields = {
        'project'   : fields.String,
        'name'   : fields.String,
        'project-url'   : fields.String,
        'description-short'  : fields.String,
        'image-url'  : fields.String,
        'video-url'  : fields.String,
        'date-published'  : fields.DateTime(dt_format='rfc822'),
        'amount' : fields.Float
    }
    required = resource_fields.keys()

@swagger.model
@swagger.nested(**{
                'top10-collaborations' : ProjectContribution.__name__,
                'top10-donations'      : ProjectContribution.__name__,
                'top10-receipts'       : ProjectAmount.__name__
                }
            )
class ProjectsResponse(Response):

    resource_fields = {
        "failed"                         : fields.Integer,
        "published"                      : fields.Integer,
        "received"                       : fields.Integer,
        "successful"                     : fields.Integer,
        "successful-completed"           : fields.Integer,
        "percentage-successful"          : fields.Float,
        "percentage-successful-completed": fields.Float,
        "average-amount-successful"      : fields.Float,
        "top10-collaborations"           : fields.List(fields.Nested(ProjectContribution.resource_fields)),
        "top10-donations"                : fields.List(fields.Nested(ProjectContribution.resource_fields)),
        "top10-receipts"                 : fields.List(fields.Nested(ProjectAmount.resource_fields)),
        "average-posts-successful"       : fields.Float
    }

    required = resource_fields.keys()


@swagger.model
class ProjectsAPI(Base):
    """Get Projects Statistics"""

    def __init__(self):
        super(ProjectsAPI, self).__init__()

    @swagger.operation(
        notes='Projects report',
        responseClass=ProjectsResponse.__name__,
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

        time_start = time.time()
        # remove not used args
        args = self.parse_args(remove=('page','limit'))

        succ_projects = Project.total(successful=True, **args)
        # succ_projects_closed = Project.total(closed=True, **args)
        succ_finished = Project.total(finished=True, **args)
        fail_projects = Project.total(failed=True, **args)

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

        top10_receipts = []
        for u in Project.received_list(finished=True, **args):
            item = marshal(u, ProjectAmount.resource_fields)
            item['description-short'] = u['subtitle']
            item['video-url'] = u['media']
            item['date-published'] = utc_from_local(u['published'])
            item['image-url'] = image_url(u['image'], 'big', False)
            item['project-url'] = project_url(u['project'])
            top10_receipts.append(item)

        res = ProjectsResponse(
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
