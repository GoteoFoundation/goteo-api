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
    "id": fields.String,
    "name": fields.String,
    "description_short": fields.String,
    "lang": fields.String,
    "node": fields.String,
    "date_created": DateTime,
    "date_published": DateTime,
    "project_url": fields.String,
    "image_url": fields.String,
    "latitude": fields.Float,
    "longitude": fields.Float,
    "region": fields.String,
    "owner": fields.String,
    "owner_name": fields.String,
    "status": fields.String,
    "minimum": fields.Float,
    "optimum": fields.Float,
    "amount": fields.Float,
}

project_gallery_resource_fields = {
    "image_url": fields.String,
    "resource_url": fields.String,
}

project_reward_resource_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "type": fields.String,
    "amount": fields.Integer,
    "icon_url": fields.String,
    "license": fields.String,
    "license_description": fields.String,
    "license_name": fields.String,
    "license_url": fields.String,
    "license_svg_url": fields.String,
}
project_reward_translate_resource_fields = project_reward_resource_fields.copy()
project_reward_translate_resource_fields.pop('type')
project_reward_translate_resource_fields.pop('icon_url')
project_reward_translate_resource_fields.pop('license_svg_url')
project_reward_translate_resource_fields.pop('license')
project_reward_translate_resource_fields.pop('id')
project_reward_translate_resource_fields.pop('amount')

project_cost_resource_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "type": fields.String,
    "amount": fields.Float,
    "required": fields.String,
    "date_from": DateTime,
    "date_to": DateTime,
}
project_cost_translate_resource_fields = {
    "name": fields.String,
    "description": fields.String,
}

project_need_resource_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "type": fields.String,
}
project_need_translate_resource_fields = {
    "name": fields.String,
    "description": fields.String,
}

project_full_resource_fields = project_resource_fields.copy()
project_full_resource_fields.pop('latitude')
project_full_resource_fields.pop('longitude')
project_full_resource_fields.pop('region')
project_full_resource_fields["description"] = fields.String
project_full_resource_fields["motivation"] = fields.String
project_full_resource_fields["goal"] = fields.String
project_full_resource_fields["about"] = fields.String
project_full_resource_fields["currency"] = fields.String
project_full_resource_fields["currency_rate"] = fields.Float
project_full_resource_fields["scope"] = fields.String
project_full_resource_fields["date_created"] = DateTime
project_full_resource_fields["date_published"] = DateTime
project_full_resource_fields["date_updated"] = DateTime
project_full_resource_fields["date_succeeded"] = DateTime
project_full_resource_fields["date_closed"] = DateTime
project_full_resource_fields["date_passed"] = DateTime
project_full_resource_fields["location"] = fields.List(fields.Nested(location_resource_fields))
project_full_resource_fields["user"] = fields.Nested(user_resource_fields)
project_full_resource_fields["widget_url"] = fields.String
project_full_resource_fields["image_url_big"] = fields.String
project_full_resource_fields["image_gallery"] = fields.List(fields.Nested(project_gallery_resource_fields))
project_full_resource_fields["video_url"] = fields.String
project_full_resource_fields["rewards"] = fields.List(fields.Nested(project_reward_resource_fields))
project_full_resource_fields["costs"] = fields.List(fields.Nested(project_cost_resource_fields))
project_full_resource_fields["needs"] = fields.List(fields.Nested(project_need_resource_fields))

project_full_translate_resource_fields = {k: v for k, v in project_full_resource_fields.items() if k in ProjectLang.get_translate_keys()}
project_full_translate_resource_fields['description_short'] = fields.String
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
            item['status'] = p.status_string
            location = ProjectLocation.get(p.id)
            if location:
                item['latitude'] = location.latitude
                item['longitude'] = location.longitude
                item['region'] = location.region if location.region != '' else location.country
            items.append(item)

        res = Response(
            starttime=time_start,
            attributes={'items': items},
            filters=args.items(),
            total=Project.total(**args)
        )

        return res


class ProjectAPI(BaseItem):
    """Project Details"""

    @requires_auth()
    @ratelimit()
    @swag_from('swagger_specs/project_item.yml')
    def get(self, project_id):
        res = self._get(project_id)

        if res.ret['id'] is None:
            return bad_request('Project not found', 404)

        return res.response()

    def _get(self, project_id):
        """Get()'s method dirty work"""
        time_start = time.time()
        p = Project.get(project_id)

        item = marshal(p, project_full_resource_fields)
        if p is not None:
            item['status'] = p.status_string
            item['scope'] = p.scope_string
            item['user'] = marshal(p.User, user_resource_fields)
            location = ProjectLocation.get(p.id)
            if location:
                item['location'] = [marshal(location, location_resource_fields)]
            gallery = ProjectImage.get(p.id)
            if gallery:
                item['image-gallery'] = []
                for i in gallery:
                    item['image-gallery'].append({
                        'image-url': image_url(i.image, 'big', False),
                        'resource-url': image_resource_url(i.url)
                        })
                #     i['image-url'] = gallery.image
            rewards = Reward.list_by_project(p.id)
            print(rewards)
            if rewards:
                item['rewards'] = marshal(rewards, project_reward_resource_fields, remove_null=True)

            costs = Cost.list_by_project(p.id)
            if costs:
                item['costs'] = marshal(costs, project_cost_resource_fields, remove_null=True)

            needs = Support.list_by_project(p.id)
            if needs:
                item['needs'] = marshal(needs, project_need_resource_fields, remove_null=True)

            translations = {}
            for k in p.Translations:
                translations[k.lang] = marshal(k, project_full_translate_resource_fields)
                rewards = Reward.list_by_project(p.id, lang=k.lang)
                if rewards:
                    translations[k.lang]['rewards'] = {}
                    for r in rewards:
                        translations[k.lang]['rewards'][r.id] = marshal(r, project_reward_translate_resource_fields, remove_null=True)

                costs = Cost.list_by_project(p.id, lang=k.lang)
                if costs:
                    translations[k.lang]['costs'] = {}
                    for r in costs:
                        translations[k.lang]['costs'][r.id] = marshal(r, project_cost_translate_resource_fields, remove_null=True)

                needs = Support.list_by_project(p.id, lang=k.lang)
                if needs:
                    translations[k.lang]['needs'] = {}
                    for r in needs:
                        translations[k.lang]['needs'][r.id] = marshal(r, project_need_translate_resource_fields, remove_null=True)

            item['translations'] = translations

        res = Response(
            starttime=time_start,
            attributes=item
        )

        return res


class ProjectDonorsListAPI(BaseList):
    """Donors list"""

    @requires_auth()
    @ratelimit()
    @swag_from('swagger_specs/project_donors.yml')
    def get(self, project_id):
        res = self._get(project_id)

        if res.ret['id'] is None:
            return bad_request('Project not found', 404)

        return res.response()

    def _get(self, project_id):
        """Get()'s method dirty work"""

        time_start = time.time()
        args = self.parse_args(remove=('location'))

        items = []
        if Project.get(project_id) is None:
            return Response(attributes={'id': None})

        for u in User.donors_by_project(project_id, **args):
            item = marshal(u, donor_resource_fields)
            item['anonymous'] = bool(u['anonymous'])
            item['node'] = u['node_id']
            item['date-created'] = u['created']
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

            items.append(item)
        res = Response(
            starttime=time_start,
            attributes={'id': project_id, 'items': items},
            filters=args.items(),
            total=User.donors_by_project_total(project_id, **args)
        )

        return res
