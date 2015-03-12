    # -*- coding: utf-8 -*-

import time
from flask.ext.restful import fields
from flask.ext.sqlalchemy import sqlalchemy
from flask_restful_swagger import swagger
from sqlalchemy import and_, or_, desc

from api.helpers import utc_from_local, image_url, project_url
from api import db
from api.models.models import Blog, Post
from api.models.project import Project, ProjectCategory
from api.models.message import Message
from api.models.invest import Invest
from api.models.location import Location, LocationItem
from api.decorators import *

from api.base_endpoint import BaseList as Base, Response


func = sqlalchemy.func

@swagger.model
class ProjectContribution:
    resource_fields = {
        'name'  : fields.String,
        'project-url'  : fields.String,
        'image-url'  : fields.String,
        'video-url'  : fields.String,
        'date-published'  : fields.DateTime(dt_format='rfc822'),
        'total' : fields.Integer
    }
    required = resource_fields.keys()

@swagger.model
class ProjectAmount:
    resource_fields = {
        'name'   : fields.String,
        'project-url'   : fields.String,
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
        time_start = time.time()
        # remove not used args
        args = self.parse_args(remove=('page','limit'))


        filters = []
        # FIXME: Qué fechas coger depende del dato: creación, finalización...
        if args['from_date']:
            filters.append(Project.published >= args['from_date'])
        if args['to_date']:
            filters.append(Project.published <= args['to_date'])
        if args['project']:
            filters.append(Project.id.in_(args['project']))
        if args['node']:
            filters.append(Project.node.in_(args['node']))
        if args['category']:
            filters.append(Project.id == ProjectCategory.project)
            filters.append(ProjectCategory.category.in_(args['category']))
        if args['location']:
            locations_ids = Location.location_ids(**args['location'])

            if locations_ids == []:
                return bad_request("No locations in the specified range")
            #TODO: change to project type 'project'
            filters.append(Project.owner == LocationItem.item)
            filters.append(LocationItem.type == 'user')
            filters.append(LocationItem.id.in_(locations_ids))

        succ_projects = self._successful(list(filters))
        succ_projects_closed = self._successful(list(filters), True)
        fail_projects = self._failed(list(filters))
        succ_finished = self._finished(list(filters))
        res = ProjectsResponse(
            starttime = time_start,
            attributes = {
                'received'                       : self._received(list(filters)),
                'published'                      : self._published(list(filters)),
                'failed'                         : fail_projects,
                'successful'                     : succ_projects,
                'successful-completed'           : succ_finished,
                'percentage-successful'          : percent(succ_projects, succ_projects_closed),
                'percentage-successful-completed' : percent(succ_finished, succ_finished + fail_projects),
                'average-amount-successful'      : self._avg_success(list(filters)),
                'average-posts-successful'       : self._avg_posts_success(list(filters)),
                'top10-collaborations'           : map(lambda p: {'name': p.name,
                                                                  'project': p.project,
                                                                  'description-short' : p.subtitle,
                                                                  'project-url' : project_url(p.project),
                                                                  'image-url' : image_url(p.image, 'big', False),
                                                                  'video-url': p.media,
                                                                  'date-published': utc_from_local(p.published)},
                                                            self._top10_collaborations(list(filters))),
                'top10-donations'                : map(lambda p: {'name': p.name,
                                                                  'project': p.project,
                                                                  'description-short' : p.subtitle,
                                                                  'project-url' : project_url(p.project),
                                                                  'image-url' : image_url(p.image, 'big', False),
                                                                  'video-url': p.media,
                                                                  'date-published': utc_from_local(p.published)},
                                                            self._top10_donations(list(filters))),
                'top10-receipts'                 : map(lambda p: {'name': p.name,
                                                                  'project': p.project,
                                                                  'description-short' : p.subtitle,
                                                                  'project-url' : project_url(p.project),
                                                                  'image-url' : image_url(p.image, 'big', False),
                                                                  'video-url': p.media,
                                                                  'date-published': utc_from_local(p.published)},
                                                            self._top10_invests(list(filters))),
            },
            filters = args.items()
        )
        return res

    # Proyectos enviados a revisión (renombrar Proyectos recibidos)
    # TODO: la fechas a revisar tiene que ser el created (published no está para proyectos en revision)
    def _received(self, f_rev_projects = []):
        f_rev_projects.append(Project.date_updated != None)
        f_rev_projects.append(Project.date_updated != '0000-00-00')
        res = db.session.query(func.count(Project.id)).filter(*f_rev_projects).scalar()
        if res is None:
            res = 0
        return res

    # Proyectos publicados
    def _published(self, f_pub_projects = []):
        f_pub_projects.append(Project.published != None)
        f_pub_projects.append(Project.published != '0000-00-00')
        f_pub_projects.append(Project.status > Project.STATUS_REJECTED)
        res = db.session.query(func.count(Project.id)).filter(*f_pub_projects).scalar()
        if res is None:
            res = 0
        return res

    # Proyectos exitosos (llegan al mínimo pueden estar en campaña)
    def _successful(self, f_succ_projects = [], closed = False):
        f_succ_projects.append(Project.status > Project.STATUS_REJECTED)
        if closed:
            and1 = and_(Project.date_passed != None, Project.date_passed != '0000-00-00')
            and2 = and_(Project.date_closed != None, Project.date_closed != '0000-00-00')
            f_succ_projects.append(or_(and1, and2))
        else :
            f_succ_projects.append(Project.date_passed != None)
            f_succ_projects.append(Project.date_passed != '0000-00-00')

        res = db.session.query(func.count(Project.id)).filter(*f_succ_projects).scalar()
        if res is None:
            res = 0
        return res


    # -Proyectos exitosos con campaña finalizada
    def _finished(self, f_succ_finished = []):
        f_succ_finished.append(Project.status.in_([Project.STATUS_FUNDED,
                                                   Project.STATUS_FULFILLED]))
        # print(f_succ_finished)
        res = db.session.query(Project).filter(*f_succ_finished).count()
        if res is None:
            res = 0
        return res


    # Proyectos archivado (Proyectos Fallidos)
    def _failed(self, f_fail_projects = []):
        f_fail_projects.append(Project.status == Project.STATUS_UNFUNDED)
        res = db.session.query(func.count(Project.id)).filter(*f_fail_projects).scalar()
        if res is None:
            res = 0
        return res

    # Media de recaudación conseguida por proyectos exitosos
    def _avg_success(self, f_p_avg_success = []):
        f_p_avg_success.append(Invest.status.in_([Invest.STATUS_CHARGED,
                                                  Invest.STATUS_PAID]))
        f_p_avg_success.append(Project.status.in_([Project.STATUS_FUNDED,
                                                   Project.STATUS_FULFILLED]))
        res = db.session.query(func.sum(Invest.amount) / func.count(func.distinct(Project.id)))\
                                    .join(Project).filter(*f_p_avg_success).scalar()
        res = 0 if res is None else round(res, 2)
        return res

    # 10 Campañas con más colaboraciones
    def _top10_collaborations(self, f_top10_collaborations = []):
        res = db.session.query(Project.id.label('project'),
                               Project.name,
                               Project.subtitle,
                               Project.image,
                               Project.media,
                               Project.published,
                               func.count(Message.id).label('total')).join(Message)\
                            .filter(*f_top10_collaborations).group_by(Message.project)\
                            .order_by(desc('total')).limit(10).all()
        if res is None:
            res = 0
        return res

    # 10 Campañas con más cofinanciadores
    def _top10_donations(self, f_top10_donations = []):
        # TODO: invest.status? project.satus?
        res = db.session.query(Project.id.label('project'),
                               Project.name,
                               Project.subtitle,
                               Project.image,
                               Project.media,
                               Project.published,
                               func.count(Invest.id).label('total')).join(Invest)\
                                    .filter(*f_top10_donations).group_by(Invest.project)\
                                    .order_by(desc('total')).limit(10).all()
        if res is None:
            res = 0
        return res


    # 10 Campañas que han recaudado más dinero
    def _top10_invests(self, f_top10_invests = []):
        f_top10_invests.append(Project.status.in_([Project.STATUS_FUNDED,
                                                   Project.STATUS_FULFILLED]))
        f_top10_invests.append(Invest.status.in_([Invest.STATUS_PENDING,
                                                  Invest.STATUS_CHARGED,
                                                  Invest.STATUS_PAID]))
        res = db.session.query(Project.id.label('project'),
                               Project.name,
                               Project.subtitle,
                               Project.image,
                               Project.media,
                               Project.published,
                               func.sum(Invest.amount).label('amount')).join(Invest)\
                                    .filter(*f_top10_invests).group_by(Invest.project)\
                                    .order_by(desc('amount')).limit(10).all()
        if res is None:
            res = 0
        return res

    # Media de posts proyecto exitoso
    def _avg_posts_success(self, f_avg_succ_posts = []):
        f_avg_succ_posts.append(Post.publish == 1)
        sq1 = db.session.query(func.count(Project.id).label('posts')).select_from(Post)\
                            .join(Blog, and_(Blog.id == Post.blog, Blog.type == 'project'))\
                            .join(Project, and_(Project.id == Blog.owner, Project.status.in_([Project.STATUS_FUNDED,
                                                                                              Project.STATUS_FULFILLED])))\
                            .filter(*f_avg_succ_posts).group_by(Post.blog).subquery()
        res = db.session.query(func.avg(sq1.c.posts)).scalar()
        res = 0 if res is None else round(res, 2)
        return res

