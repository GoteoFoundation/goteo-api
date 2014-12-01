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

        # -  [Renombrar dinero comprometido] Suma recaudada por la plataforma
        comprometido = db.session.query(Invest.project, func.sum(Invest.amount)).filter(*filters).group_by(Invest.project).limit(limit).all()

        # TODO: ??
        recaudado = db.session.query(func.sum(Invest.amount)).filter(*filters).scalar()

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
        # TODO: Comprobar
        #fee = recaudado * 0.08
        #recaudado = db.session.query(func.sum(Invest.amount)).filter(*filters).scalar()
        # select from success_projects
        fee_amount = db.session.query

        # - Aporte medio por cofinanciador(micromecenas)
        # TODO
        # SELECT avg(amount) as a FROM `invest` group by user
        #average-invest = db.session.query(func.avg(Invest.amount)).filter(*call_filter).group_by(Invest.user).scalar()
        # Average per user
        sub1 = db.session.query(func.avg(Invest.amount).label('amount')).filter(*filters).\
                                        group_by(Invest.user).subquery()
        average_invest = db.session.query(func.avg(sub1.c.amount)).scalar()

        # - Aporte medio por cofinanciador(micromecenas) mediante PayPal
        # TODO
        avg_paypal = filters
        avg_paypal.append(Invest.method==Invest.METHOD_PAYPAL)
        average_invest_paypal = db.session.query(func.avg(Invest.amount)).filter(*avg_paypal).group_by(Invest.user).scalar()

        # - (Renombrar Coste mínimo medio por proyecto exitoso ] Presupuesto mínimo medio por proyecto exitoso
        # TODO

        # - Recaudación media por proyecto exitoso ( financiado )
        # TODO

        # - Perc. medio de recaudación sobre el mínimo (número del dato anterior)
        # TODO

        # (Nuevo) Dinero medio solo obtenido en 2a ronda
        # TODO

        # - [Renombrar Dinero compr. medio en proyectoss archivados] Dinero recaudado de media en campañas fallidas
        # TODO

        # - [Renombrar]Perc.   dinero compr. medio (dinero recaudado de media) sobre mínimo (número del dato anterior)
        # TODO

        app.logger.debug('end sql')

        if comprometido is None or recaudado is None or devuelto is None:
            abort(404)

        app.logger.debug('end check')
        # TypeError: Decimal('1420645') is not JSON serializable
        # No se pueden donar centimos no? Hacer enteros?
        #return {'total': int(total_recaudado[0])}
        return jsonify({'total': int(recaudado), 'devuelto': int(devuelto), 'limit-per-page': limit,
                        'paypal-amount': paypal_amount, 'tpv-amount': tpv_amount, 'cash-amount': cash_amount,
                        'call-amount': call_amount, 'average-invest': average_invest,
                        'projects': map(lambda i: [i[0], {'recaudado': i[1]}], comprometido)})

        #return {'total': str(total_recaudado[0])}

        #return {'total': total_recaudado[0], 'projects': invests}
        #return jsonify(invests)
        #return {'invests': map(lambda i: {i[0]: i[1]}, invests)}
        #return {'invests': {'pliegos': suma}}
        #return {'invests': map(lambda i: {i.investid: marshal(i, invest_fields)}, invests)}
