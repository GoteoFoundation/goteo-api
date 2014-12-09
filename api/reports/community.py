# -*- coding: utf-8 -*-
from model import app, db
from model import Invest, User, Category, Message, Project, UserInterest

from flask import abort, jsonify
from flask.ext.restful import Resource, reqparse, fields, marshal
from flask.ext.sqlalchemy import sqlalchemy
from flask_restful_swagger import swagger

from sqlalchemy import desc


@swagger.model
class CommunityResponse:
    """CommunityResponse"""

    __name__ = "CommunityResponse"

    resource_fields = {
        "categoria1": fields.String,
        "categoria2": fields.String,
        "categorias": fields.List,
        "cofinanciadores": fields.Integer,
        "colaboradores": fields.Integer,
        "coficolaboradores": fields.Integer,
        "impulcofinanciadores": fields.Integer,
        "impulcolaboradores": fields.Integer,
        "media-cofi": fields.Float,
        "media-colab": fields.Float,
        "multicofi": fields.Integer,
        "paypal": fields.Integer,
        "paypal-multicofi": fields.Integer,
        "perc-bajas": fields.Float,
        "perc-categoria1": fields.Float,
        "perc-categoria2": fields.Float,
        "users": fields.Integer,
        "users-cofi-perc": fields.Float,
        "users-multicofi-perc": fields.Float,
        "top10-cofi": fields.List,
        "top10-cofi2": fields.List,
        "top10-colab": fields.List
    }

    required = []


class CommunityAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('from_date', type=str)
        self.reqparse.add_argument('to_date', type=str)
        self.reqparse.add_argument('node', type=str, action='append')
        self.reqparse.add_argument('project', type=str, action='append')
        super(CommunityAPI, self).__init__()

    invalid_input = {
        "code": 400,
        "message": "Invalid parameters"
    }

    @swagger.operation(
    summary='Community report',
    notes='Community report',
    responseClass='CommunityResponse',
    nickname='community',
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
        """Get the Community Report

        Descripción de los valores devueltos:
        <strong>users</strong>: Número total de usuarios registrados
        <strong>perc-bajas</strong>: Porcentaje de usuarios que se han dado de baja
        <strong>cofinanciadores</strong>: Número de cofinanciadores
        <strong>users-cofi-perc</strong>: % usuarios registrados que son cofinanciadores
        <strong>coficolaboradores</strong>: Número de cofinanciadores que colaboran
        <strong>multicofi</strong>: Número de Multi-Cofinanciadores (a más de 1 proyecto)
        <strong>users-multicofi-perc</strong>: % de Multi-Cofinanciadores (a más de 1 proyecto)
        <strong>paypal</strong>: Número de cofinanciadores que usan PayPal
        <strong>paypal-multicofi</strong>: Número de Multi-Cofinanciadores que usan PayPal
        <strong>colaboradores</strong>: Número de colaboradores
        <strong>media-cofi</strong>: Media de cofinanciadores por proyecto exitoso
        <strong>media-colab</strong>: Media de colaboradores por proyecto
        <strong>impulcofinanciadores</strong>: Número de impulsores que cofinancian a otros
        <strong>impulcolaboradores</strong>: Número de impulsores que colaboran con otros
        <strong>categoria1</strong>: 1ª categoría con más usuarios interesados
        <strong>perc-categoria1</strong>: % usuarios en esta 1ª categoría
        <strong>categoria2</strong>: 2ª categoría con más usuarios interesados
        <strong>perc-categoria2</strong>: % usuarios en esta 2ª categoría
        <strong>top10-cofi</strong>: Top 10 cofinanciadores
        <strong>top10-cofi2</strong>: Top 10 cofinanciadores con más caudal (más generosos) sin incluir usuarios convocadores
        <strong>top10-colab</strong>: Top 10 colaboradores

        <strong>categorias</strong>:

        Además se añade el campo "filters"
        """
        func = sqlalchemy.func
        args = self.reqparse.parse_args()

        filters = []
        if args['from_date']:
            filters.append(Invest.date_invested >= args['from_date'])
        if args['to_date']:
            filters.append(Invest.date_invested <= args['to_date'])
        if args['project']:
            filters.append(Invest.project.in_(args['project']))
        if args['node']:
            pass

        # - Número total de usuarios formados en Goteo (num de proyectos enviados a revisión + inscrito talleres )
        # TODO
        # Inscritos en talleres no se puede saber. Project.updated o estado > 1, Negociación o posterior.
        # Campo owner de projectos con status > 1. PD: Estado 1 draft, contarlos? Y status < 6 (descartado)

        # - Número total de usuarios
        users = db.session.query(User).filter(*filters).count()

        def perc_users(number):
            perc = float(number) / users * 100
            return round(perc, 2)

        # - Porcentaje (antes numero) de usuarios que se han dado de baja
        # FIXME: # Active=0, hide=1 + todos los datos borrados (2)
        f_bajas = list(filters)
        f_bajas.append(User.active == 0)
        bajas = db.session.query(User).filter(*f_bajas).count()
        p_bajas = perc_users(bajas)

        # - Número de cofinanciadores
        _cofinanciadores = db.session.query(func.distinct(Invest.user)).filter(*filters) # .subquery()
        cofinanciadores = _cofinanciadores.count()

        # - NEW Porcentaje de usuarios cofinanciadores
        users_cofi_perc = perc_users(cofinanciadores)
        #users_cofi_perc = float(cofinanciadores) / users * 100  # %
        #users_cofi_perc = _round(users_cofi_perc)

        app.logger.debug('multicofi')
        # - Multi-Cofinanciadores (a más de 1 proyecto)
        # FIXME: filters: WHERE invest.status IN (0, 1, 3, 4)
        _multicofi = db.session.query(Invest.user).filter(*filters).group_by(Invest.user).\
                                                    having(func.count(Invest.user) > 1).\
                                                    having(func.count(Invest.project) > 1)
        multicofi = _multicofi.count()

        # - NEW Porcentaje de Multi-Cofinanciadores (a más de 1 proyecto)
        users_multicofi_perc = perc_users(multicofi)

        # - Cofinanciadores usando PayPal
        f_paypal = list(filters)
        f_paypal.append(Invest.method==Invest.METHOD_PAYPAL)
        paypal = db.session.query(Invest).filter(*f_paypal).count()

        # - Multi-Cofinanciadores usando PayPal
        f_paypal_multicofi = list(filters)
        f_paypal_multicofi.append(Invest.method==Invest.METHOD_PAYPAL)
        paypal_multicofi = _multicofi.filter(*f_paypal_multicofi).count()

        # - Número de colaboradores
        f_colaboradores = list(filters)
        _colaboradores = db.session.query(func.distinct(Message.user)).filter(*filters).subquery()
        colaboradores = _colaboradores.count()

        # - Cofinanciadores que colaboran
        # FIXME: WHERE invest.status IN (0, 1, 3, 4)? reporting.php
        sq = db.session.query(Message.id).filter(Message.blocked == 1).subquery()
        f_coficolaboradores = list(filters)
        f_coficolaboradores.append(Message.thread > 0)
        f_coficolaboradores.append(Message.thread.in_(sq))
        coficolaboradores = db.session.query(func.count(func.distinct(Invest.user)))\
                                            .join(Message, Message.user == Invest.user)\
                                            .filter(*f_coficolaboradores).scalar()

        # - Media de cofinanciadores por proyecto exitoso
        f_media_cofi = list(filters)
        f_media_cofi.append(Project.status.in_([4, 5]))
        sq = db.session.query(func.count(func.distinct(Invest.user)).label("co"))\
                                    .join(Project, Invest.project == Project.id)\
                                    .filter(*f_media_cofi).group_by(Invest.project).subquery()
        media_cofi = db.session.query(func.avg(sq.c.co)).scalar()

        # - Media de colaboradores por proyecto
        # FIXME: exitoso? Cuando es exitoso y cuando no?
        f_media_colab = list(filters)
        f_media_colab.append(Project.status.in_([4, 5]))
        sq = db.session.query(func.count(func.distinct(Message.user)).label("co"))\
                                    .join(Project, Message.project == Project.id)\
                                    .filter(*f_media_colab).group_by(Message.project).subquery()
        media_colab = db.session.query(func.avg(sq.c.co)).scalar()

        # - Núm. impulsores que cofinancian a otros
        # FIXME:
        # AND project.status IN (3, 4, 5, 6)
        # WHERE invest.status IN (0, 1, 3, 4)
        # AND invest.project != project.id
        impulcofinanciadores = db.session.query(func.count(func.distinct(Project.owner)))\
                                                .join(Invest, Invest.user == Project.owner)\
                                                .filter(*filters).scalar()

        # - Núm. impulsores que colaboran con otros
        sq = db.session.query(Message.id).filter(Message.blocked == 1).subquery()
        f_impulcolaboradores = list(filters)
        f_impulcolaboradores.append(Message.thread > 0)
        f_impulcolaboradores.append(Message.thread.in_(sq))
        f_impulcolaboradores.append(Message.project != Project.id)
        # FIXME: project.status IN (3, 4, 5, 6)
        impulcolaboradores = db.session.query(func.count(func.distinct(Project.owner)))\
                                                .join(Message, Message.user == Project.owner)\
                                                .filter(*f_impulcolaboradores).scalar()



        # - 1ª Categoría con más usuarios interesados
        categorias = db.session.query(func.count(UserInterest.user), Category.name)\
                        .join(Category).group_by(UserInterest.interest)\
                        .order_by(desc(func.count(UserInterest.user))).all()

        categoria1 = categorias[0][1]

        # - Porcentaje de usuarios en esta 1ª
        perc_categoria1 = perc_users(categorias[0][0])

        # - 2ª Categoría con más usuarios interesados
        categorias2 = categorias[1][1]

        # - Porcentaje de usuarios en esta 2ª
        perc_categoria2 = perc_users(categorias[1][0])

        # - Top 10 Cofinanciadores (REVISAR como sacamos estos datos, excepto admines)
        # TODO

        # - Top 10 Cofinanciadores con más caudal (más generosos) excluir usuarios convocadores Y ADMINES
        # TODO

        # - Top 10 colaboradores
        # TODO

        def format_categorias(t):
            total = t[0]
            name = t[1]
            perc = float(total) / users * 100
            perc = round(perc, 2)
            return {name: {'interesados': total, 'porcentaje': perc}}

        res = {'users': users,
                'users-cofi-perc': users_cofi_perc, 'multicofi': multicofi,
                'users-multicofi-perc': users_multicofi_perc, 'paypal': paypal,
                'paypal-multicofi': paypal_multicofi, 'perc-bajas': p_bajas,
                'colaboradores': colaboradores,
                'impulcofinanciadores': impulcofinanciadores,
                'impulcolaboradores': impulcolaboradores,
                'coficolaboradores': coficolaboradores,
                'media-cofi': media_cofi, 'media-colab': media_colab,
                'categorias': map(lambda i: format_categorias(i), categorias),
                'categoria1': categorias[0][1], 'categoria2': categorias[1][1],
                'perc-categoria1': perc_categoria1, 'perc-categoria2': perc_categoria2}
                #'categories': ['a','b']})

        res['filters'] = {}
        for k, v in args.items():
            if v is not None:
                res['filters'][k] = v

        return jsonify(res)
