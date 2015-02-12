# -*- coding: utf-8 -*-

import time
from flask import jsonify
from flask.ext.restful import Resource, fields
from flask.ext.sqlalchemy import sqlalchemy
from flask_restful_swagger import swagger
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import and_, or_, desc

from config import config

from api.model import db,Blog, Category, Invest, Message, Post, Project, ProjectCategory
from api.model import Location, LocationItem
from api.decorators import *

from api.reports.base import Base, Response

# DEBUG
if config.debug:
    db.session.query = debug_time(db.session.query)

func = sqlalchemy.func

@swagger.model
class ProjectContribution:
    resource_fields = {
        'name'  : fields.String,
        'total' : fields.Integer
    }
    required = resource_fields.keys()

@swagger.model
class ProjectAmount:
    resource_fields = {
        'name'   : fields.String,
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
        <a href="http://developers.goteo.org/reports#projects">developers.goteo.org/reports#projects</a>
        """
        time_start = time.time()
        args = self.reqparse.parse_args()

        filters = []
        # FIXME: Qué fechas coger depende del dato: creación, finalización...
        if args['from_date']:
            filters.append(Project.date_published >= args['from_date'])
        if args['to_date']:
            filters.append(Project.date_published <= args['to_date'])
        if args['project']:
            filters.append(Project.id.in_(args['project']))
        if args['node']:
            filters.append(Project.node.in_(args['node']))
        if args['category']:
            try:
                category_id = db.session.query(Category.id).filter(Category.name == args['category']).one()
                category_id = category_id[0]
            except NoResultFound:
                return bad_request("Invalid category")

            filters.append(Project.id == ProjectCategory.project)
            filters.append(ProjectCategory.category == category_id)
        if args['location']:
            location = args['location'].split(",")
            if len(location) != 3:
                return bad_request("Invalid parameter: location")

            from geopy.distance import VincentyDistance
            latitude, longitude, radius = location

            radius = int(radius)
            if radius > 500 or radius < 0:
                return bad_request("Radius must be a value between 0 and 500 Km")

            locations = db.session.query(Location.id, Location.lat, Location.lon).all()
            locations = filter(lambda l: VincentyDistance((latitude, longitude), (l[1], l[2])).km <= radius, locations)
            locations_ids = map(lambda l: int(l[0]), locations)

            if locations_ids == []:
                return bad_request("No locations in the specified range")

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
                'top10-collaborations'           : self._top10_collaborations(list(filters)),
                'top10-donations'                : self._top10_donations(list(filters)),
                'top10-receipts'                 : self._top10_invests(list(filters)),
            },
            filters = args.items()
        )
        return res.response()

    # Proyectos enviados a revisión (renombrar Proyectos recibidos)
    def _received(self, f_rev_projects = []):
        f_rev_projects.append(Project.date_updated != None)
        f_rev_projects.append(Project.date_updated != '0000-00-00')
        res = db.session.query(func.count(Project.id)).filter(*f_rev_projects).scalar()
        if res is None:
            res = 0
        return res

    # Proyectos publicados
    def _published(self, f_pub_projects = []):
        f_pub_projects.append(Project.date_published != None)
        f_pub_projects.append(Project.date_published != '0000-00-00')
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
                                                   Project.STATUS_FULLFILED]))
        print(f_succ_finished)
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
                                                   Project.STATUS_FULLFILED]))
        res = db.session.query(func.sum(Invest.amount) / func.count(func.distinct(Project.id)))\
                                    .join(Project).filter(*f_p_avg_success).scalar()
        res = 0 if res is None else round(res, 2)
        return res

    # 10 Campañas con más colaboraciones
    def _top10_collaborations(self, f_top10_collaborations = []):
        res = db.session.query(Project.id.label('project'), func.count(Message.id).label('total')).join(Message)\
                            .filter(*f_top10_collaborations).group_by(Message.project)\
                            .order_by(desc('total')).limit(10).all()
        if res is None:
            res = 0
        return res

    # 10 Campañas con más cofinanciadores
    def _top10_donations(self, f_top10_donations = []):
        # FIXME: invest.status?
        res = db.session.query(Project.id.label('project'), func.count(Invest.id).label('total')).join(Invest)\
                                    .filter(*f_top10_donations).group_by(Invest.project)\
                                    .order_by(desc('total')).limit(10).all()
        if res is None:
            res = 0
        return res


    # 10 Campañas que han recaudado más dinero
    def _top10_invests(self, f_top10_invests = []):
        f_top10_invests.append(Project.status.in_([Project.STATUS_FUNDED,
                                                   Project.STATUS_FULLFILED]))
        f_top10_invests.append(Invest.status.in_([Invest.STATUS_PENDING,
                                                  Invest.STATUS_CHARGED,
                                                  Invest.STATUS_PAID]))
        res = db.session.query(Project.id.label('project'), func.sum(Invest.amount).label('amount')).join(Invest)\
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
                                                                                              Project.STATUS_FULLFILED])))\
                            .filter(*f_avg_succ_posts).group_by(Post.blog).subquery()
        res = db.session.query(func.avg(sq1.c.posts)).scalar()
        res = 0 if res is None else round(res, 2)
        return res

