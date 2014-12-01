# -*- coding: utf-8 -*-
from model import app, db
from model import Invest, User, Category, Message, Project, UserInterest

from flask import abort, jsonify
from flask.ext.restful import Resource, reqparse, fields, marshal
from flask.ext.sqlalchemy import sqlalchemy
from flask_restful_swagger import swagger

from sqlalchemy import desc

class ModelClass():
    pass


@swagger.model
class CommunityAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('from_date', type=str)
        self.reqparse.add_argument('to_date', type=str)
        self.reqparse.add_argument('limit', type=int, default=10)
        self.reqparse.add_argument('project', type=str, action='append')
        super(CommunityAPI, self).__init__()

    @swagger.operation(
    notes='Community report',
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
        if args['from_date']:
            filters.append(Invest.date_invested >= args['from_date'])
        if args['to_date']:
            filters.append(Invest.date_invested <= args['to_date'])
        if args['project']:
            filters.append(Invest.project.in_(args['project']))
        limit = args['limit']

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

        app.logger.debug('end check')

        return jsonify({'users': users,
                        'users-cofi-perc': users_cofi_perc, 'multicofi': multicofi,
                        'users-multicofi-perc': users_multicofi_perc, 'paypal': paypal,
                        'paypal-multicofi': paypal_multicofi, 'perc-bajas': p_bajas,
                        'impulcofinanciadores': impulcofinanciadores,
                        'impulcolaboradores': impulcolaboradores,
                        'coficolaboradores': coficolaboradores,
                        'media-cofi': media_cofi, 'media-colab': media_colab,
                        #'categorias': categorias})
                        'categorias': map(lambda i: {i[1]: {'interesados': i[0], 'porcentaje': float(i[0]) / users * 100}}, categorias),
                        'categoria1': categorias[0][1], 'categoria2': categorias[1][1],
                        'perc-categoria1': perc_categoria1, 'perc-categoria2': perc_categoria2})
                        #'categories': ['a','b']})
