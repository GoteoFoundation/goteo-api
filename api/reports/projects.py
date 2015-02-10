# -*- coding: utf-8 -*-
from model import app, db
from model import Blog, Category, Invest, Message, Post, Project, ProjectCategory
from model import Location, LocationItem

from flask import abort, jsonify
from flask.ext.restful import Resource, reqparse, fields, marshal
from flask.ext.sqlalchemy import sqlalchemy
from flask_restful_swagger import swagger
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import and_, or_, desc

from decorators import *
from config import config

import time

# DEBUG
if config.debug:
    db.session.query = debug_time(db.session.query)


@swagger.model
class ProjectsResponse:

    __name__ = "ProjectsResponse"

    resource_fields = {
        "failed": fields.Integer,
        "published": fields.Integer,
        "received": fields.Integer,
        "succesful": fields.Integer,
        "successful-percentage": fields.Float,
        "successful-finished": fields.Integer,
        "successful-finished-perc": fields.Float,
        "average-success-percentage": fields.Float,
        "top10-investors": fields.List,
        "top10-collaborations": fields.List,
        "top10-invests": fields.List,
        "average-successful-posts": fields.Float,
    }

    required = resource_fields.keys()


@swagger.model
class ProjectsAPI(Resource):
    """Get Projects Statistics"""

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('from_date', type=str)
        self.reqparse.add_argument('to_date', type=str)
        self.reqparse.add_argument('node', type=str, action='append')
        self.reqparse.add_argument('project', type=str, action='append')
        self.reqparse.add_argument('category', type=str)
        self.reqparse.add_argument('location', type=str)
        super(ProjectsAPI, self).__init__()

    invalid_input = {
        "code": 400,
        "message": "Invalid parameters"
    }

    @swagger.operation(
    summary='Projects report',
    notes='Projects report',
    responseClass='ProjectsResponse',
    nickname='projects',
    parameters=[
        {
            "paramType": "query",
            "name": "project",
            "description": "Filter by individual project(s) separated by commas",
            "required": False,
            "dataType": "string",
            "allowMultiple": True
        },
        {
            "paramType": "query",
            "name": "from_date",
            "description": 'Filter from date. Ex. "2013-01-01"',
            "required": False,
            "dataType": "string"
        },
        {
            "paramType": "query",
            "name": "to_date",
            "description": 'Filter until date.. Ex. "2014-01-01"',
            "required": False,
            "dataType": "string"
        },
        {
            "paramType": "query",
            "name": "node",
            "description": 'Filter by individual node(s) separated by commas',
            "required": False,
            "dataType": "string"
        },
        {
            "paramType": "query",
            "name": "category",
            "description": 'Filter by project category',
            "required": False,
            "dataType": "string"
        },
        {
            "paramType": "query",
            "name": "location",
            "description": 'Filter by projects location of project owner (Lat,lon,Km)',
            "required": False,
            "dataType": "string"
        }

    ],
    responseMessages=[invalid_input])
    @requires_auth
    @ratelimit()
    def get(self):
        """Get the Projects Report
        <a href="http://developers.goteo.org/reports#projects">developers.goteo.org/reports#projects</a>
        """
        time_start = time.time()
        func = sqlalchemy.func
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
                return {"error": "Invalid category"}, 400

            filters.append(Project.id == ProjectCategory.project)
            filters.append(ProjectCategory.category == category_id)
        if args['location']:
            location = args['location'].split(",")
            if len(location) != 3:
                return {"error": "Invalid parameter: location"}, 400

            from geopy.distance import VincentyDistance
            latitude, longitude, radius = location

            radius = int(radius)
            if radius > 500 or radius < 0:
                return {"error": "Radius must be a value between 0 and 500 Km"}, 400

            locations = db.session.query(Location.id, Location.lat, Location.lon).all()
            locations = filter(lambda l: VincentyDistance((latitude, longitude), (l[1], l[2])).km <= radius, locations)
            locations_ids = map(lambda l: int(l[0]), locations)

            if locations_ids == []:
                return {"error": "No locations in the specified range"}, 400

            filters.append(Project.owner == LocationItem.item)
            filters.append(LocationItem.type == 'user')
            filters.append(LocationItem.id.in_(locations_ids))

        # - Proyectos enviados a revisión (renombrar Proyectos recibidos)
        f_rev_projects = list(filters)
        f_rev_projects.append(Project.date_updated != None)
        f_rev_projects.append(Project.date_updated != '0000-00-00')
        rev_projects = db.session.query(func.count(Project.id)).filter(*f_rev_projects).scalar()

        # - Proyectos publicados
        f_pub_projects = list(filters)
        f_pub_projects.append(Project.date_published != None)
        f_pub_projects.append(Project.date_published != '0000-00-00')
        f_pub_projects.append(Project.status > 0)
        pub_projects = db.session.query(func.count(Project.id)).filter(*f_pub_projects).scalar()

        # - Proyectos exitosos (llegan al mínimo pueden estar en campaña)
        f_succ_projects = list(filters)
        f_succ_projects.append(Project.date_passed != None)
        f_succ_projects.append(Project.date_passed != '0000-00-00')
        f_succ_projects.append(Project.status > 0)
        succ_projects = db.session.query(func.count(Project.id)).filter(*f_succ_projects).scalar()

        # Publicados y cerrados
        f_pub_projects2 = list(filters)
        f_pub_projects2.append(Project.status > 0)
        and1 = and_(Project.date_passed != None, Project.date_passed != '0000-00-00')
        and2 = and_(Project.date_closed != None, Project.date_closed != '0000-00-00')
        f_pub_projects2.append(or_(and1, and2))
        pub_projects2 = db.session.query(func.count(Project.id)).filter(*f_pub_projects2).scalar()

        # -(nuevo) proyectos exitosos con campaña finalizada
        f_succ_finished = list(filters)
        f_succ_finished.append(Project.status.in_([config.PROJECT_STATUS_FUNDED,
                                                   config.PROJECT_STATUS_FULLFILED]))
        succ_finished = db.session.query(Project).filter(*f_succ_finished).count()

        # - Proyectos archivados Renombrar por Proyectos Fallidos
        f_fail_projects = list(filters)
        f_fail_projects.append(Project.status == config.PROJECT_STATUS_UNFUNDED)
        fail_projects = db.session.query(func.count(Project.id)).filter(*f_fail_projects).scalar()

        # - Media de recaudación conseguida por proyectos exitosos
        f_p_avg_success = list(filters)
        f_p_avg_success.append(Invest.status.in_([config.INVEST_STATUS_CHARGED,
                                                  config.INVEST_STATUS_PAID]))
        f_p_avg_success.append(Project.status.in_([config.PROJECT_STATUS_FUNDED,
                                                   config.PROJECT_STATUS_FULLFILED]))
        avg_success = db.session.query(func.sum(Invest.amount) / func.count(func.distinct(Project.id)))\
                                    .join(Project).filter(*f_p_avg_success).scalar()
        avg_success = 0 if avg_success is None else round(avg_success, 2)

        # - 10 Campañas con más colaboraciones
        f_top10_collaborations = list(filters)
        top10_collaborations = db.session.query(Project.id.label('project'), func.count(Message.id).label('total')).join(Message)\
                            .filter(*f_top10_collaborations).group_by(Message.project)\
                            .order_by(desc('total')).limit(10).all()

        # - 10 Campañas con más cofinanciadores
        # FIXME: invest.status?
        f_top10_donations = list(filters)
        top10_donations = db.session.query(Project.id.label('project'), func.count(Invest.id).label('total')).join(Invest)\
                                    .filter(*f_top10_donations).group_by(Invest.project)\
                                    .order_by(desc('total')).limit(10).all()

        # - 10 Campañas que han recaudado más dinero
        f_top10_invests = list(filters)
        f_top10_invests.append(Project.status.in_([config.PROJECT_STATUS_FUNDED,
                                                   config.PROJECT_STATUS_FULLFILED]))
        f_top10_invests.append(Invest.status.in_([config.INVEST_STATUS_PENDING,
                                                  config.INVEST_STATUS_CHARGED,
                                                  config.INVEST_STATUS_PAID]))
        top10_invests = db.session.query(Project.id.label('project'), func.sum(Invest.amount).label('amount')).join(Invest)\
                                    .filter(*f_top10_invests).group_by(Invest.project)\
                                    .order_by(desc('amount')).limit(10).all()

        # - Media de posts proyecto exitoso
        f_avg_succ_posts = list(filters)
        f_avg_succ_posts.append(Post.publish == 1)
        sq1 = db.session.query(func.count(Project.id).label('posts')).select_from(Post)\
                            .join(Blog, and_(Blog.id == Post.blog, Blog.type == 'project'))\
                            .join(Project, and_(Project.id == Blog.owner, Project.status.in_([config.PROJECT_STATUS_FUNDED,
                                                                                              config.PROJECT_STATUS_FULLFILED])))\
                            .filter(*f_avg_succ_posts).group_by(Post.blog).subquery()
        avg_succ_posts = db.session.query(func.avg(sq1.c.posts)).scalar()
        avg_succ_posts = 0 if avg_succ_posts is None else round(avg_succ_posts, 2)

        res = { 'received': rev_projects,
                'published': pub_projects,
                'failed': fail_projects,
                'successful': succ_projects,
                'percentage-successful': percent(succ_projects, pub_projects2),
                'successful-complete': succ_finished,
                'percentage-successful-complete': percent(succ_finished, succ_finished + fail_projects),
                'top10-collaborations': top10_collaborations,
                'top10-donations': top10_donations,
                'top10-receipts': top10_invests,
                'average-amount-successful': avg_success,
                'average-posts-successful': avg_succ_posts
              }

        res['time-elapsed'] = time.time() - time_start
        res['filters'] = {}
        for k, v in args.items():
            if v is not None:
                res['filters'][k] = v

        return jsonify(res)
