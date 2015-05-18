# -*- coding: utf-8 -*-

import time

from flask.ext.restful import fields, marshal
from flask_restful_swagger import swagger

from ..decorators import *
from ..base_resources import BaseItem, BaseList, Response

from .models import Project
from ..location.models import ProjectLocation

@swagger.model
class ProjectResponse(Response):
    """ProjectResponse"""

    resource_fields = {
        "id"                : fields.String,
        "name"              : fields.String,
        "node"              : fields.String,
        "date-created"      : fields.DateTime(dt_format='rfc822'), # iso8601 maybe?
        "date-published"    : fields.DateTime(dt_format='rfc822'), # iso8601 maybe?
        "project-url"       : fields.String,
        "image-url" : fields.String,
        "latitude" : fields.Float,
        "longitude" : fields.Float,
    }

    required = resource_fields.keys()

@swagger.model
class ProjectGalleryResponse(Response):
    """ProjectGalleryResponse"""

    resource_fields = {
        "name"              : fields.String,
        "node"              : fields.String,
        "date-created"      : fields.DateTime(dt_format='rfc822'), # iso8601 maybe?
        "date-published"    : fields.DateTime(dt_format='rfc822'), # iso8601 maybe?
        "project-url"       : fields.String,
        "image-url" : fields.String,
    }

    required = resource_fields.keys()

@swagger.model
class ProjectLocationResponse(Response):
    """ProjectLocationResponse"""

    resource_fields = {
        "city"              : fields.String,
        "region"              : fields.String,
        "country"              : fields.String,
        "country_code"              : fields.String,
        "latitude" : fields.Float,
        "longitude" : fields.Float,
    }

    required = resource_fields.keys()


@swagger.model
class ProjectCompleteResponse(Response):
    """ProjectCompleteResponse"""

    resource_fields = {
        "id"                : fields.String,
        "name"              : fields.String,
        "description-short" : fields.String,
        "node"              : fields.String,
        "date-created"      : fields.DateTime(dt_format='rfc822'),
        "date-published"    : fields.DateTime(dt_format='rfc822'),
        # "date-updated"    : fields.DateTime(dt_format='rfc822'),
        "location" : fields.List(fields.Nested(ProjectLocationResponse.resource_fields)),
        "project-url"       : fields.String,
        "widget-url"       : fields.String,
        "image-url" : fields.String,
        "image-url-big" : fields.String,
        "image-gallery" : fields.List(fields.String),
        "video-url" : fields.String,
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
        args = self.parse_args()

        items = []
        for p in Project.list(**args):
            item = marshal(p, ProjectResponse.resource_fields)
            item['date-created'] =p.date_created
            item['date-published'] = p.date_published
            item['project-url'] = project_url(p.id)
            item['image-url'] = image_url(p.image, 'medium', False)
            location = ProjectLocation.get(p.id)
            if location:
                item['latitude'] = location.latitude
                item['longitude'] = location.longitude
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
        p = Project.get(project_id)

        item = marshal(p, ProjectCompleteResponse.resource_fields)
        if p != None:
            item['date-created'] = p.date_created
            item['date-published'] = p.date_published
            item['description-short'] = p.subtitle
            item['video-url'] = p.media
            item['image-url'] = image_url(p.image, 'medium', False)
            item['image-url-big'] = image_url(p.image, 'big', False)
            item['project-url'] = project_url(p.id)
            item['widget-url'] = project_widget_url(p.id)
            location = ProjectLocation.get(p.id)
            if location:
                item['location'] = marshal(location, ProjectLocationResponse.resource_fields)
            #     item['latitude'] = location.latitude
            #     item['longitude'] = location.longitude


        res = ProjectCompleteResponse(
            starttime = time_start,
            attributes = item
        )

        return res

