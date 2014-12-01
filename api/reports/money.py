# -*- coding: utf-8 -*-
from model import app, db
from model import Project, Invest, Call, Cost

from flask import abort, jsonify
from flask.ext.restful import Resource, reqparse, fields, marshal
from flask.ext.sqlalchemy import sqlalchemy
from flask_restful_swagger import swagger

from datetime import date

invest_fields = {
    'id': fields.Integer,
    'user': fields.String,
    'project': fields.String,
    'status': fields.Integer,
    'amount': fields.Integer
}

@swagger.model
class MoneyResponse:

    __name__ = "MoneyResponse"

    resource_fields = {
        'total': fields.Integer,
        'devuelto': fields.Integer,
        'results-per-page': fields.Integer,
        'paypal-amount': fields.Integer,
        'tpv-amount': fields.Integer,
        'cash-amount': fields.Integer,
        'call-amount': fields.Integer,
        'average-invest': fields.Integer,
        'projects': fields.List,
        'fee-amount': fields.Integer,
        'to_date': fields.String,
        'limit': fields.Integer,
    }


#@swagger.model
class MoneyAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('from_date', type=str)
        self.reqparse.add_argument('to_date', type=str)
        self.reqparse.add_argument('limit', type=int, default=10)
        self.reqparse.add_argument('offset', type=int, default=0)
        self.reqparse.add_argument('project', type=str, action='append')
        super(MoneyAPI, self).__init__()

    successful = {
        "code": 200,
         "message": "OK"
    }

    invalid_input = {
        "code": 404,
         "message": "Not found"
    }

    @swagger.operation(
    notes='Money report',
    responseClass='MoneyResponse',
    #nickname='get',
    parameters=[
        {
            "paramType": "query",
            "name": "project",
            "description": "Filter by individual project(s)",
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
            "name": "limit",
            "description": "Number of projects per page. Default = 10",
            "required": False,
            "dataType": "integer"
        },
        {
            "paramType": "query",
            "name": "offset",
            "description": "Number of projects per page. Default = 0",
            "required": False,
            "dataType": "integer"
        }
    ],
    responseMessages=[successful, invalid_input])
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
            #filters.append(Invest.project.in_(args['project'][0]))
            filters.append(Invest.project.in_(args['project']))
        limit = args['limit']
        #filters = and_(*filters)

        print(filters)
        app.logger.debug('start sql')

        #
        # Proyectos exitosos
        #
        success_projects = Project.query.filter(Project.status.in_([4,5])).subquery()

        # TODO: ??
        recaudado = db.session.query(func.sum(Invest.amount)).filter(*filters).scalar()

        # -  [Renombrar dinero comprometido] Suma recaudada por la plataforma
        comprometido = db.session.query(Invest.project, func.sum(Invest.amount)).filter(*filters).group_by(Invest.project).limit(limit).all()

        # TODO: Qué mostrar cuando no hay resultados?
        if recaudado is None:
            return jsonify({})

        # - Dinero devuelto (en proyectos archivados)
        devuelto_filter = list(filters)
        devuelto_filter.append(Project.id==Invest.project)
        devuelto_filter.append(Project.status==4)
        devuelto = db.session.query(func.sum(Invest.amount)).filter(*devuelto_filter).scalar()

        #- Recaudado mediante PayPal
        paypal_filter = list(filters)
        paypal_filter.append(Invest.method==Invest.METHOD_PAYPAL)
        paypal_amount = db.session.query(func.sum(Invest.amount)).filter(*paypal_filter).scalar()

        #- Recaudado mediante TPV
        tpv_filter = list(filters)
        tpv_filter.append(Invest.method==Invest.METHOD_TPV)
        tpv_amount = db.session.query(func.sum(Invest.amount)).filter(*tpv_filter).scalar()

        # - [Renombrar aportes manuales] Recaudado mediante transferencia bancaria directa
        cash_filter = list(filters)
        cash_filter.append(Invest.method==Invest.METHOD_CASH)
        cash_amount = db.session.query(func.sum(Invest.amount)).filter(*cash_filter).scalar()

        # - [Renombrar] Capital Riego de Goteo (fondos captados de instituciones y empresas destinados a la bolsa de Capital Riego https://goteo.org/service/resources)
        # TODO: Comprobar que es correcto. Quitar las convocatorias de prueba que hay en la BD!!
        #call_amount = db.session.query(func.sum(Call.amount)).filter(*filters).scalar()

        # - [NEW] Suma recaudada en Convocatorias (Capital riego distribuido + crowd)
        # FIXME: Invest.method==DROP + invest.call==1 ?
        call_filter = list(filters)
        call_filter.append(Invest.method==Invest.METHOD_DROP)
        call_amount = db.session.query(func.sum(Invest.amount)).filter(*call_filter).scalar()

        # - Total 8% recaudado por Goteo
        f_fee_amount = list(filters)
        f_fee_amount.append(Project.status.in_([4, 5]))
        f_fee_amount.append(Invest.status.in_([1, 3]))
        fee_amount = db.session.query(func.sum(Invest.amount)).join(Project).filter(*f_fee_amount).scalar()
        fee_amount = float(fee_amount) * 0.08

        # - Aporte medio por cofinanciador(micromecenas)
        # OJO: En reporting.php no calcula esto mismo
        # FIXME: No deberían contar también los proyectos archivados?
        f_avg_invest = list(filters)
        f_avg_invest.append(Project.status.in_([4, 5]))
        f_avg_invest.append(Invest.status.in_([1, 3]))
        sub1 = db.session.query(func.avg(Invest.amount).label('amount')).join(Project)\
                                        .filter(*f_avg_invest).group_by(Invest.user).subquery()
        average_invest = db.session.query(func.avg(sub1.c.amount)).scalar()
        average_invest = round(average_invest, 2)

        # - Aporte medio por cofinanciador(micromecenas) mediante PayPal
        # OJO: En reporting.php no calcula esto mismo
        # FIXME: No deberían contar también los proyectos archivados?
        f_avg_paypal = list(f_avg_invest)
        f_avg_paypal.append(Invest.method==Invest.METHOD_PAYPAL)
        sub1 = db.session.query(func.avg(Invest.amount).label('amount')).join(Project)\
                                        .filter(*f_avg_paypal).group_by(Invest.user).subquery()
        average_invest_paypal = db.session.query(func.avg(sub1.c.amount)).scalar()
        average_invest_paypal = 0 if average_invest_paypal is None else round(average_invest_paypal, 2)

        # - (Renombrar Coste mínimo medio por proyecto exitoso ] Presupuesto mínimo medio por proyecto exitoso
        # OJO: En reporting.php no calcula esto mismo
        # FIXME: No debería excluir el 6?
        f_avg_cost = list(filters)
        f_avg_cost.append(Cost.required == 1)
        f_avg_cost.append(Project.status.in_([3, 4, 5, 6]))
        sub2 = db.session.query(func.avg(Cost.amount).label("amount")).join(Project, Project.id == Cost.project)\
                                    .filter(*f_avg_cost).group_by(Cost.project).subquery()
        average_cost = db.session.query(func.avg(sub2.c.amount)).scalar()
        average_cost = round(average_cost, 2)

        # - Recaudación media por proyecto exitoso ( financiado )
        f_avg_minimum = list(filters)
        f_avg_minimum.append(Invest.status.in_([1, 3]))
        f_avg_minimum.append(Project.status.in_([4, 5]))
        average_minimum = db.session.query(func.sum(Invest.amount) / func.count(func.distinct(Project.id)))\
                                    .join(Project).filter(*f_avg_minimum).scalar()
        average_minimum = round(average_minimum, 2)

        # - Perc. medio de recaudación sobre el mínimo (número del dato anterior)
        f_comprometido_success = list(filters)
        f_comprometido_success.append(Invest.status.in_([1, 3]))
        f_comprometido_success.append(Project.status.in_([4, 5]))
        sub = db.session.query((func.sum(Invest.amount) / Project.minimum * 100 - 100).label('percent'))\
                            .select_from(Invest).join(Project)\
                            .filter(*f_comprometido_success).group_by(Invest.project).subquery()
        comprometido_success = db.session.query(func.avg(sub.c.percent)).scalar()
        comprometido_success = round(comprometido_success, 2)

        # (Nuevo) Dinero medio solo obtenido en 2a ronda
        f_avg_second_round = list(filters)
        f_avg_second_round.append(Invest.date_invested >= Project.date_passed)
        sub = db.session.query(func.sum(Invest.amount).label('amount')).join(Project)\
                                            .filter(*f_avg_second_round).group_by(Project.id).subquery()
        avg_second_round = db.session.query(func.avg(sub.c.amount)).scalar()
        avg_second_round = round(avg_second_round, 2)

        # - [Renombrar Dinero compr. medio en proyectos archivados] Dinero recaudado de media en campañas fallidas
        f_avg_failed = list(filters)
        f_avg_failed.append(Project.status == 6)
        f_avg_failed.append(Invest.status.in_([0, 4]))
        avg_failed = db.session.query(func.sum(Invest.amount) / func.count(func.distinct(Project.id)))\
                                        .join(Project).filter(*f_avg_failed).scalar()
        avg_failed = round(avg_failed, 2)

        # - [Renombrar]Perc. dinero compr. medio (dinero recaudado de media) sobre mínimo (número del dato anterior)
        # Perc. dinero compr. medio sobre mínimo',
        f_comprometido_fail = list(filters)
        f_comprometido_fail.append(Invest.status.in_([0, 4]))
        f_comprometido_fail.append(Project.status == 6)
        sub = db.session.query((func.sum(Invest.amount) / Project.minimum * 100).label('percent'))\
                            .select_from(Invest).join(Project)\
                            .filter(*f_comprometido_fail).group_by(Invest.project).subquery()
        comprometido_fail = db.session.query(func.avg(sub.c.percent)).scalar()
        comprometido_fail = round(comprometido_fail, 2)


        # No se pueden donar centimos no? Hacer enteros?
        return jsonify({'total': int(recaudado), 'devuelto': int(devuelto), 'results-per-page': limit,
                        'paypal-amount': paypal_amount, 'tpv-amount': tpv_amount, 'cash-amount': cash_amount,
                        'call-amount': call_amount, 'average-invest': average_invest,
                        'projects': map(lambda i: [i[0], {'recaudado': i[1]}], comprometido),
                        'fee-amount': fee_amount, 'average-cost': average_cost})

        #return {'invests': map(lambda i: {i.investid: marshal(i, invest_fields)}, invests)}
