# -*- coding: utf-8 -*-

import time

from flask.ext.restful import fields, marshal
from flask_restful_swagger import swagger

from ..decorators import *
from ..base_resources import BaseItem, BaseList, Response

from .models import Project

@swagger.model
class ProjectResponse(Response):
    """ProjectResponse"""

    resource_fields = {
        "id"                : fields.String,
        "name"              : fields.String,
        "node"              : fields.String,
        "date-created"      : fields.DateTime(dt_format='rfc822'), # iso8601 maybe?
        "profile-url"       : fields.String,
        "profile-image-url" : fields.String,
    }

    required = resource_fields.keys()


@swagger.model
class ProjectCompleteResponse(Response):
    """ProjectCompleteResponse"""

    resource_fields = {
        "id"                : fields.String,
        "name"              : fields.String,
        "node"              : fields.String,
        "date-created"      : fields.DateTime(dt_format='rfc822'),
        # "date-updated"    : fields.DateTime(dt_format='rfc822'),
        "profile-url"       : fields.String,
        "profile-image-url" : fields.String,
    }

    required = resource_fields.keys()

@swagger.model
@swagger.nested(**{
                'items' : ProjectResponse.__name__,
                }
            )
class ProjectsListResponse(Response):
    """ProjectsListResponse"""

    resource_fields = {
        "items"         : fields.List(fields.Nested(ProjectResponse.resource_fields)),
    }

    required = resource_fields.keys()


class ProjectsListAPI(BaseList):
    """Get Project list"""


    @swagger.operation(
        notes='Projects list',
        nickname='projects',
        responseClass=ProjectsListResponse.__name__,
        parameters=BaseList.INPUT_FILTERS,
        responseMessages=BaseList.RESPONSE_MESSAGES
    )
    @requires_auth
    @ratelimit()
    def get(self):
        """Get the projects list
        <a href="http://developers.goteo.org/doc/projects">developers.goteo.org/doc/projects</a>
        """
        res = self._get()

        if res.ret['items'] == []:
            return bad_request('No projects to list', 404)

        return res.response()

    def _get(self):
        """Get()'s method dirty work"""

        time_start = time.time()
        # For privacy, removing location filter ?
        args = self.parse_args(remove=('location'))

        items = []
        for u in Project.list(**args):
            item = marshal(u, ProjectResponse.resource_fields)
            item['date-created'] = u.date_created
            item['profile-url'] = u.profile_url
            item['profile-image-url'] = u.profile_image_url
            items.append( item )

        res = ProjectsListResponse(
            starttime = time_start,
            attributes = {'items' : items},
            filters = args.items(),
            total = Project.total(**args)
        )

        return res



class ProjectAPI(BaseItem):
    """Get Project Details"""

    @swagger.operation(
        notes='Project profile',
        nickname='project',
        responseClass=ProjectCompleteResponse.__name__,
        responseMessages=BaseItem.RESPONSE_MESSAGES
    )
    @requires_auth
    @ratelimit()
    def get(self, project_id):
        """Get a project details
        <a href="http://developers.goteo.org/projects#project">developers.goteo.org/projects#project</a>
        """
        res = self._get(project_id)

        if res.ret['id'] == None:
            return bad_request('Project not found', 404)

        return res.response()

    def _get(self, project_id):
        """Get()'s method dirty work"""
        time_start = time.time()
        u = Project.get(project_id)
        item = marshal(u, ProjectCompleteResponse.resource_fields)
        if u != None:
            item['date-created'] = u.date_created
            item['profile-url'] = u.profile_url
            item['profile-image-url'] = u.profile_image_url

        res = ProjectCompleteResponse(
            starttime = time_start,
            attributes = item
        )

        return res

