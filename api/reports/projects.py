# -*- coding: utf-8 -*-
from model import app, db
from model import Project, Invest, Blog, Post

from flask import abort, jsonify
from flask.ext.restful import Resource, reqparse, fields, marshal
from flask.ext.sqlalchemy import sqlalchemy
from flask_restful_swagger import swagger

from sqlalchemy import and_, or_


class ModelClass():
    pass


@swagger.model
class ProjectsAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('from_date', type=str)
        self.reqparse.add_argument('to_date', type=str)
        self.reqparse.add_argument('limit', type=int, default=10)
        self.reqparse.add_argument('project', type=str, action='append')
        super(ProjectsAPI, self).__init__()

    @swagger.operation(
    notes='Projects report',
    responseClass=ModelClass.__name__,
    nickname='upload',
    responseMessages=[
        {
          "code": 200,
          "message": "OK"
        },
        {
          "code": 404,
          "message": "Not found"
        }
      ]
    )
    def get(self):
        func = sqlalchemy.func
        args = self.reqparse.parse_args()

        print args
        app.logger.debug('projects')
        app.logger.debug(args['project'])

        filters = []
        # TODO: Qué fechas coger? creacion, finalizacion?
        if args['from_date']:
            filters.append(Invest.date_invested >= args['from_date'])
        if args['to_date']:
            filters.append(Invest.date_invested <= args['to_date'])
        if args['project']:
            filters.append(Invest.project.in_(args['project'][0]))
        limit = args['limit']

        app.logger.debug('start sql')

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
        f_succ_projects = list(filters)
        f_succ_projects.append(Project.date_passed is not None)
        f_succ_projects.append(Project.date_passed != '0000-00-00')
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

        # -(nuevo) proyectos exitosos con campaña finalizada
        # TODO

        # _(nuevo)% éxito campañas finalizadas
        # TODO

        # - Proyectos archivados Renombrar por Proyectos Fallidos
        f_fail_projects = list(filters)
        f_fail_projects.append(Project.status == 6)
        fail_projects = db.session.query(func.count(Project.id)).filter(*f_fail_projects).scalar()

        # - Porcentaje media de recaudación conseguida por proyectos exitosos
        # TODO
        """
            'label' => 'Recaudación media por proyecto exitoso',
            'sql'   => "SELECT SUM(invest.amount) / COUNT(DISTINCT(project.id))
                        FROM invest
                        INNER JOIN project
                            ON  project.id = invest.project
                            AND project.status IN (4, 5)
                        WHERE invest.status IN (1, 3)
                        :investfilter
                        ",
        """

        # - (NUEVOS)10 Campañas con más cofinanciadores
        f_top10_projects = list(filters)
        top10_projects = db.session.query(func.count(Invest.id)).filter(*f_top10_projects).group_by(Invest.project).limit(10).all()

        # - 10 Campañas con más colaboraciones
        f_top10_projects2 = list(filters)

        # - 10 Campañas que han recaudado más dinero
        f_top10_projects3 = list(filters)

        # - Campañas más rápidas en conseguir el mínimo (NUEVO)
        # TODO
        # Contar Invest.date_invested ordenadas que suman Project.minimum. Coger el que tenga menos dias. ¿10?
        # Lo que pasa es que va a haber primero proyectos de poco dinero.

        # - Media de posts proyecto exitoso
        # Project.status 4,5
        # AVG(blog)

        app.logger.debug('end check')

        return jsonify({'rev-projects': rev_projects, 'pub-projects': pub_projects,
                        'succ-projects': succ_projects, 'perc-succ-projects': p_succ_projects,
                        'fail-projects': fail_projects})
