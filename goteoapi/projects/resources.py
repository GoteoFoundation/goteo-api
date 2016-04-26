# -*- coding: utf-8 -*-

import time
from flask.ext.restful import fields
from flasgger.utils import swag_from

from ..ratelimit import ratelimit
from ..auth.decorators import requires_auth
from ..helpers import *

from ..base_resources import BaseItem, BaseList, Response
from .models import Project, ProjectImage, ProjectLang
from ..users.models import User
from ..users.resources import user_resource_fields
from ..location.models import ProjectLocation, UserLocation, location_resource_fields
from ..models.reward import Reward
from ..models.cost import Cost
from ..models.support import Support

project_resource_fields = {
    "id"                : fields.String,
    "name"              : fields.String,
    "description_short" : fields.String,
    "lang" : fields.String,
    "node"              : fields.String,
    "date_created"      : DateTime,
    "date_published"    : DateTime,
    "project_url"       : fields.String,
    "image_url" : fields.String,
    "latitude" : fields.Float,
    "longitude" : fields.Float,
    "region" : fields.String,
    "owner" : fields.String,
    "owner_name" : fields.String,
    "status" : fields.String,
    "minimum" : fields.Float,
    "optimum" : fields.Float,
    "amount" : fields.Float,
}

project_gallery_resource_fields = {
    "image_url" : fields.String,
    "resource_url" : fields.String,
}

project_reward_resource_fields = {
    "reward" : fields.String,
    "description"              : fields.String,
    "license"              : fields.String,
    "type"              : fields.String,
    "icon"              : fields.String,
}

project_cost_resource_fields = {
    "cost" : fields.String,
    "description"              : fields.String,
    "type"              : fields.String,
    "amount"              : fields.Float,
    "required"              : fields.String,
    "date_from"              : DateTime,
    "date_to"              : DateTime,
}

project_need_resource_fields = {
    "support" : fields.String,
    "description"              : fields.String,
    "type"              : fields.String,
}

project_full_resource_fields = {
    "id"                : fields.String,
    "name"              : fields.String,
    "description_short" : fields.String,
    "description" : fields.String,
    "motivation" : fields.String,
    "goal" : fields.String,
    "about" : fields.String,
    "lang" : fields.String,
    "currency" : fields.String,
    "currency_rate" : fields.Float,
    "minimum" : fields.Float,
    "optimum" : fields.Float,
    "amount" : fields.Float,
    "status" : fields.String,
    "scope" : fields.String,
    "node"              : fields.String,
    "date_created"      : DateTime,
    "date_published"    : DateTime,
    "date_updated"    : DateTime,
    "date_succeeded"    : DateTime,
    "date_closed"    : DateTime,
    "date_passed"    : DateTime,
    "location" : fields.List(fields.Nested(location_resource_fields)),
    "owner" : fields.String,
    "user" : fields.Nested(user_resource_fields),
    "project_url"       : fields.String,
    "widget_url"       : fields.String,
    "image_url" : fields.String,
    "image_url_big" : fields.String,
    "image_gallery" : fields.List(fields.Nested(project_gallery_resource_fields)),
    "video_url" : fields.String,
    "rewards" : fields.List(fields.Nested(project_reward_resource_fields)),
    "costs" : fields.List(fields.Nested(project_cost_resource_fields)),
    "needs" : fields.List(fields.Nested(project_need_resource_fields))
}

donor_resource_fields = user_resource_fields.copy()
donor_resource_fields['anonymous'] = fields.Boolean

class ProjectsListAPI(BaseList):
    """Project list"""

    @requires_auth()
    @ratelimit()
    @swag_from('swagger_specs/project_list.yml')
    def get(self):
        res = self._get()

        return res.response()

    def _get(self):
        """Get()'s method dirty work"""

        time_start = time.time()
        args = self.parse_args()

        items = []
        for p in Project.list(**args):
            item = marshal(p, project_resource_fields)
            item['project-url'] = project_url(p.id)
            item['description-short'] = p.subtitle
            item['status'] = p.status_string
            item['image-url'] = image_url(p.image, 'medium', False)
            location = ProjectLocation.get(p.id)
            if location:
                item['latitude'] = location.latitude
                item['longitude'] = location.longitude
                item['region'] = location.region if location.region != '' else location.country
            items.append( item )

        res = Response(
            starttime = time_start,
            attributes = {'items' : items},
            filters = args.items(),
            total = Project.total(**args)
        )

        return res



class ProjectAPI(BaseItem):
    """Project Details"""

    @requires_auth()
    @ratelimit()
    @swag_from('swagger_specs/project_item.yml')
    def get(self, project_id):
        res = self._get(project_id)

        if res.ret['id'] == None:
            return bad_request('Project not found', 404)

        return res.response()

    def _get(self, project_id):
        """Get()'s method dirty work"""
        time_start = time.time()
        p = Project.get(project_id)

        item = marshal(p, project_full_resource_fields)
        if p != None:
            item['description-short'] = p.subtitle
            item['video-url'] = p.media
            item['image-url'] = image_url(p.image, 'medium', False)
            item['image-url-big'] = image_url(p.image, 'big', False)
            item['project-url'] = project_url(p.id)
            item['widget-url'] = project_widget_url(p.id)
            item['status'] = p.status_string
            item['scope'] = p.scope_string
            location = ProjectLocation.get(p.id)
            if location:
                item['location'] = [marshal(location, location_resource_fields)]
            gallery = ProjectImage.get(p.id)
            if gallery:
                item['image-gallery'] = []
                for i in gallery:
                    item['image-gallery'].append({
                        'image-url' : image_url(i.image, 'big', False),
                        'resource-url' : image_resource_url(i.url)
                        })
                #     i['image-url'] = gallery.image
            rewards = Reward.list_by_project(p.id)
            if rewards:
                item['rewards'] = marshal(rewards, project_reward_resource_fields)
            costs = Cost.list_by_project(p.id)
            if costs:
                item['costs'] = marshal(costs, project_cost_resource_fields)
            needs = Support.list_by_project(p.id)
            if needs:
                item['needs'] = marshal(needs, project_need_resource_fields)

            translations = {}
            translate_keys = {k: v for k, v in project_full_resource_fields.items() if k in ProjectLang.get_translate_keys()}
            for k in p.translations:
                translations[k.lang] = marshal(k, translate_keys)
                translations[k.lang]['description-short'] = k.subtitle
                translations[k.lang]['video-url'] = k.media
            item['translations'] = translations

        res = Response(
            starttime = time_start,
            attributes = item
        )

        return res


class ProjectDonorsListAPI(BaseList):
    """Donors list"""

    @requires_auth()
    @ratelimit()
    @swag_from('swagger_specs/project_donors.yml')
    def get(self, project_id):
        res = self._get(project_id)

        if res.ret['id'] == None:
            return bad_request('Project not found', 404)

        return res.response()

    def _get(self, project_id):
        """Get()'s method dirty work"""

        time_start = time.time()
        args = self.parse_args(remove=('location'))

        items = []
        if Project.get(project_id) == None:
            return Response(attributes = {'id': None})

        for u in User.donors_by_project(project_id, **args):
            item = marshal(u, donor_resource_fields)
            item['profile-image-url'] = image_url(u['avatar'])
            item['profile-url'] = user_url(u['id'])
            if u['anonymous']:
                item['id'] = None
                item['name'] = 'Anonymous'
                item['profile-image-url'] = None
                item['profile-url'] = None
            elif 'latitude' in donor_resource_fields:
                location = UserLocation.get(u['id'])
                if location:
                    item['latitude'] = location.latitude
                    item['longitude'] = location.longitude
                    item['region'] = location.region if location.region != '' else location.country

            items.append( item )
        res = Response(
            starttime = time_start,
            attributes = {'id':project_id, 'items' : items},
            filters = args.items(),
            total = User.donors_by_project_total(project_id, **args)
        )

        return res
