    # -*- coding: utf-8 -*-

import time
from flask.ext.restful import fields, marshal
from flasgger.utils import swag_from
from goteoapi.decorators import ratelimit
from goteoapi.auth.decorators import requires_auth
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
        super().__init__()

    @requires_auth
    @ratelimit()
    @swag_from('swagger_specs/projects.yml')
    def get(self):
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
