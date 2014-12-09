# -*- coding: utf-8 -*-
from model import app, db
from model import Project, Invest, Blog, Post, Message

from flask import abort, jsonify
from flask.ext.restful import Resource, reqparse, fields, marshal
from flask.ext.sqlalchemy import sqlalchemy
from flask_restful_swagger import swagger

from sqlalchemy import and_, or_, desc


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
        "top10-fastest": fields.List,
        "average-successful-posts": fields.Float,
    }


@swagger.model
class ProjectsAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('from_date', type=str)
        self.reqparse.add_argument('to_date', type=str)
        self.reqparse.add_argument('node', type=str, action='append')
        self.reqparse.add_argument('project', type=str, action='append')
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
        }

    ],
    responseMessages=[invalid_input])
    def get(self):
        """Get the Projects Report

        Descripción de los valores devueltos:
        <strong>failed</strong>: Proyectos fallidos
        <strong>published</strong>: Proyectos publicados
        <strong>received</strong>: Proyectos recibidos (enviados a revisión)
        <strong>succesful</strong>: Proyectos exitosos (alcanzaron el mínimo)
        <strong>successful-percentage</strong>: % de proyectos exitosos
        <strong>successful-finished</strong>: Número de proyectos exitosos con campaña finalizada
        <strong>successful-finished-perc</strong>: % éxito campañas finalizadas
        <strong>top10-collaborations</strong>: Las 10 campañas con más colaboraciones
        <strong>top10-investors</strong>: Las 10 campañas con más cofinanciadores
        <strong>top10-invests</strong>: Las 10 campañas que han recaudado más dinero
        <strong>average-success-percentage</strong>: % de recaudación media conseguida por proyectos exitosos
        <strong>top10-fastest</strong>: Las 10 campañas más rápidas en conseguir el mínimo
        <strong>average-successful-posts</strong>: Media de posts en proyectos exitosos

        Además se añade el campo "filters"
        """
        func = sqlalchemy.func
        args = self.reqparse.parse_args()

        filters = []
        # FIXME: Qué fechas coger depende del dato: creación, finalización...
        if args['from_date']:
            filters.append(Invest.date_invested >= args['from_date'])
        if args['to_date']:
            filters.append(Invest.date_invested <= args['to_date'])
        if args['project']:
            filters.append(Invest.project.in_(args['project'][0]))
        if args['node']:
            pass

        # - Proyectos enviados a revisión (renombrar Proyectos recibidos)
        f_rev_projects = list(filters)
        f_rev_projects.append(Project.date_updated is not None)
        f_rev_projects.append(Project.date_updated != '0000-00-00')
        rev_projects = db.session.query(func.count(Project.id)).filter(*f_rev_projects).scalar()

        # - Proyectos publicados
        f_pub_projects = list(filters)
        f_pub_projects.append(Project.date_published is not None)
        f_pub_projects.append(Project.date_published != '0000-00-00')
        f_pub_projects.append(Project.status > 0)
        pub_projects = db.session.query(func.count(Project.id)).filter(*f_pub_projects).scalar()

        # - Proyectos exitosos (llegan al mínimo pueden estar en campaña)
        # FIXME: (Project.status > 0)
        f_succ_projects = list(filters)
        f_succ_projects.append(Project.date_passed is not None)
        f_succ_projects.append(Project.date_passed != '0000-00-00')
        #f_succ_projects.append(Project.status.in_([3, 4, 5]))
        f_succ_projects.append(Project.status > 0)
        succ_projects = db.session.query(func.count(Project.id)).filter(*f_succ_projects).scalar()

        # % exito exitosos
        f_pub_projects2 = list(filters)
        f_pub_projects2.append(Project.status > 0)
        and1 = and_(Project.date_passed != None, Project.date_passed != '0000-00-00')
        and2 = and_(Project.date_closed != None, Project.date_closed != '0000-00-00')
        f_pub_projects2.append(or_(and1, and2))
        pub_projects2 = db.session.query(func.count(Project.id)).filter(*f_pub_projects2).scalar()
        p_succ_projects = float(succ_projects) / pub_projects2 * 100
        p_succ_projects = round(p_succ_projects, 2)

        # -(nuevo) proyectos exitosos con campaña finalizada
        # FIXME: correcto?
        f_succ_finished = list(filters)
        f_succ_finished.append(Project.status == 4)
        succ_finished = db.session.query(Project).filter(*f_succ_finished).count()

        # - Proyectos archivados Renombrar por Proyectos Fallidos
        f_fail_projects = list(filters)
        f_fail_projects.append(Project.status == 6)
        fail_projects = db.session.query(func.count(Project.id)).filter(*f_fail_projects).scalar()

        # _(nuevo)% éxito campañas finalizadas
        # FIXME: correcto?
        p_succ_finished = float(succ_finished) / (succ_finished + fail_projects)
        p_succ_finished = round(p_succ_finished, 2)

        # - Porcentaje media de recaudación conseguida por proyectos exitosos
        f_p_avg_success = list(filters)
        f_p_avg_success.append(Invest.status.in_([1, 3]))
        f_p_avg_success.append(Project.status.in_([4, 5]))
        p_avg_success = db.session.query(func.sum(Invest.amount) / func.count(func.distinct(Project.id)))\
                                    .join(Project).filter(*f_p_avg_success).scalar()
        p_avg_success = round(p_avg_success, 2)

        # - (NUEVOS)10 Campañas con más cofinanciadores
        f_top10_investors = list(filters)
        top10_investors = db.session.query(Project.id, func.count(Invest.id).label('total')).join(Invest)\
                                    .filter(*f_top10_investors).group_by(Invest.project)\
                                    .order_by(desc('total')).limit(10).all()

        # - 10 Campañas con más colaboraciones
        f_top10_collaborations = list(filters)
        top10_collaborations = db.session.query(Project.id, func.count(Message.id).label('total')).join(Message)\
                            .filter(*f_top10_collaborations).group_by(Message.project)\
                            .order_by(desc('total')).limit(10).all()

        # - 10 Campañas que han recaudado más dinero
        # FIXME: correcto?
        f_top10_invests = list(filters)
        f_top10_invests.append(Project.status == 4)
        f_top10_invests.append(Invest.status.in_([0, 1, 3]))
        top10_invests = db.session.query(Project.id, func.sum(Invest.amount).label('total')).join(Invest)\
                                    .filter(*f_top10_invests).group_by(Invest.project)\
                                    .order_by(desc('total')).limit(10).all()

        # - Campañas más rápidas en conseguir el mínimo (NUEVO)
        # TODO
        # Contar Invest.date_invested ordenadas que suman Project.minimum. Coger el que tenga menos dias. ¿10?
        # Lo que pasa es que va a haber primero proyectos de poco dinero.

        # - Media de posts proyecto exitoso
        # TODO
        # Project.status 4,5
        # AVG(blog)
        """
        array(
            'label' => 'Media de posts proyecto exitoso',
            'sql'   => "SELECT (
                                SELECT SUM(posts)
                                FROM (
                                    SELECT COUNT(post.id) as posts
                                    FROM post
                                    INNER JOIN blog
                                        ON   blog.id = post.blog
                                        AND  blog.type = 'project'
                                    INNER JOIN project
                                        ON  project.id = blog.owner
                                        AND project.status IN (4, 5)
                                    WHERE post.publish = 1
                                    GROUP BY post.blog
                                    ) as temp1
                            )
                            / (
                                SELECT COUNT(*)
                                FROM (
                                    SELECT project.id
                                    FROM post
                                    INNER JOIN blog
                                        ON   blog.id = post.blog
                                        AND  blog.type = 'project'
                                    INNER JOIN project
                                        ON  project.id = blog.owner
                                        AND project.status IN (4, 5)
                                    WHERE post.publish = 1
                                    GROUP BY post.blog
                                    ) as numero_proyectos
                            ) as average
                        FROM dual
                        ",
        """

        res = {'received': rev_projects, 'published': pub_projects,
                'succesful': succ_projects, 'successful-percentage': p_succ_projects,
                'failed': fail_projects, 'top10-investors': top10_investors,
                'top10-collaborations': top10_collaborations, 'top10-invests': top10_invests}

        res['filters'] = {}
        for k, v in args.items():
            if v is not None:
                res['filters'][k] = v

        return jsonify(res)
