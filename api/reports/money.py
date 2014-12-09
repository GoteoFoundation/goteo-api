# -*- coding: utf-8 -*-
from model import app, db
from model import Project, Invest, Call, Cost, InvestNode

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
    """MoneyResponse"""
    __name__ = "MoneyResponse"

    resource_fields = {
        "average-failed": fields.Float,
        "average-invest": fields.Float,
        "average-invest-paypal": fields.Float,
        "average-mincost": fields.Float,
        "average-received": fields.Float,
        "average-second-round": fields.Float,
        "call-amount": fields.Integer,
        "call-committed-amount": fields.Integer,
        "cash-amount": fields.Integer,
        "committed": fields.Integer,
        "comprometido-fail": fields.Float,
        "comprometido-success": fields.Float,
        "devuelto": fields.Integer,
        "fee-amount": fields.Float,
        "paypal-amount": fields.Integer,
        "tpv-amount": fields.Integer
    }


class MoneyAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('from_date', type=str)
        self.reqparse.add_argument('to_date', type=str)
        self.reqparse.add_argument('node', type=str, action='append')
        self.reqparse.add_argument('project', type=str, action='append')
        super(MoneyAPI, self).__init__()

    invalid_input = {
        "code": 400,
        "message": "Invalid parameters"
    }

    @swagger.operation(
    summary='Money report',
    notes='Money report',
    responseClass='MoneyResponse',
    nickname='money',
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
        """Get the Money Report

        Descripción de los valores devueltos:
        <strong>average-failed</strong>: Recaudación media por proyectos que no alcanzaron el mínimo
        <strong>average-invest</strong>: Aportación media por cofinanciador (micromecenas)
        <strong>average-invest-paypal</strong>: Aportación media por cofinanciador (micromecenas) a través de PayPal
        <strong>average-mincost</strong>: Coste medio de los proyectos exitosos
        <strong>average-received</strong>: Recaudación media por proyectos exitosos (que sí alcanzaron el mínimo)
        <strong>average-second-round</strong>: Recaudación media en segunda ronda
        <strong>call-amount</strong>: Suma recaudada en Convocatorias (Capital riego distribuido + crowd)
        <strong>call-committed-amount</strong>: Capital Riego de Goteo (fondos captados de instituciones y empresas destinados a la bolsa de <a href="https://goteo.org/service/resources">Capital Riego</a>)
        <strong>cash-amount</strong>: Suma recaudada mediante transferencia bancaria directa
        <strong>committed</strong>: Suma recaudada por la plataforma
        <strong>comprometido-fail</strong>: Porcentaje de recaudación media sobre el mínimo en proyectos fallidos
        <strong>comprometido-success</strong>: Porcentaje de recaudación media sobre el mínimo en proyectos exitosos
        <strong>devuelto</strong>: Dinero devuelto (en proyectos archivados)
        <strong>fee-amount</strong>: Total 8% recaudado por Goteo
        <strong>paypal-amount</strong>: Suma recaudada mediante PayPal
        <strong>tpv-amount</strong>: Suma recaudada mediante TPV

        Además se añade el campo "filters"
        """
        func = sqlalchemy.func
        args = self.reqparse.parse_args()

        filters = []
        filters2 = [] # para average_mincost
        if args['from_date']:
            filters.append(Invest.date_invested >= args['from_date'])
            filters2.append(Invest.date_invested >= args['from_date'])
        if args['to_date']:
            filters.append(Invest.date_invested <= args['to_date'])
            filters2.append(Invest.date_invested <= args['to_date'])
        if args['project']:
            filters.append(Invest.project.in_(args['project']))
            filters2.append(Project.id.in_(args['project']))
        if args['node']:
            filters.append(Invest.id == InvestNode.invest_id)
            filters2.append(Project.id == InvestNode.project_id)
            filters.append(InvestNode.invest_node.in_(args['node']))
            filters2.append(InvestNode.invest_node.in_(args['node']))

        #
        # Proyectos exitosos
        #
        success_projects = Project.query.filter(Project.status.in_([4,5])).subquery()

        # TODO: ??
        #recaudado = db.session.query(func.sum(Invest.amount)).filter(*filters).scalar()

        # -  [Renombrar dinero comprometido] Suma recaudada por la plataforma
        #comprometido = db.session.query(Invest.project, func.sum(Invest.amount)).filter(*filters).group_by(Invest.project).limit(limit).all()
        f_comprometido = list(filters)
        f_comprometido.append(Invest.status.in_([0, 1, 3, 4]))
        comprometido = db.session.query(func.sum(Invest.amount)).filter(*f_comprometido).scalar()
        if comprometido is None:
            comprometido = 0

        # TODO: Qué mostrar cuando no hay resultados?
        # return jsonify({})

        # - Dinero devuelto (en proyectos archivados)
        f_devuelto = list(filters)
        f_devuelto.append(Invest.status==4)
        devuelto = db.session.query(func.sum(Invest.amount)).filter(*f_devuelto).scalar()
        if devuelto is None:
            devuelto = 0

        #- Recaudado mediante PayPal
        f_paypal_amount = list(filters)
        f_paypal_amount.append(Invest.method==Invest.METHOD_PAYPAL)
        paypal_amount = db.session.query(func.sum(Invest.amount)).filter(*f_paypal_amount).scalar()
        if paypal_amount is None:
            paypal_amount = 0

        #- Recaudado mediante TPV
        f_tpv_amount = list(filters)
        f_tpv_amount.append(Invest.method==Invest.METHOD_TPV)
        tpv_amount = db.session.query(func.sum(Invest.amount)).filter(*f_tpv_amount).scalar()
        if tpv_amount is None:
            tpv_amount = 0

        # - [Renombrar aportes manuales] Recaudado mediante transferencia bancaria directa
        f_cash_amount = list(filters)
        f_cash_amount.append(Invest.method==Invest.METHOD_CASH)
        cash_amount = db.session.query(func.sum(Invest.amount)).filter(*f_cash_amount).scalar()
        if cash_amount is None:
            cash_amount = 0

        # - [Renombrar] Capital Riego de Goteo (fondos captados de instituciones y empresas destinados a la bolsa de Capital Riego https://goteo.org/service/resources)
        # TODO: Comprobar que es correcto. Quitar las convocatorias de prueba que hay en la BD!!
        #call_amount = db.session.query(func.sum(Call.amount)).filter(*filters).scalar()

        # - [NEW] Suma recaudada en Convocatorias (Capital riego distribuido + crowd)
        # FIXME: Invest.method==DROP + invest.call==1 ?
        f_call_amount = list(filters)
        f_call_amount.append(Invest.method==Invest.METHOD_DROP)
        call_amount = db.session.query(func.sum(Invest.amount)).filter(*f_call_amount).scalar()
        if call_amount is None:
            call_amount = 0

        # - Total 8% recaudado por Goteo
        f_fee_amount = list(filters)
        f_fee_amount.append(Project.status.in_([4, 5]))
        f_fee_amount.append(Invest.status.in_([1, 3]))
        fee_amount = db.session.query(func.sum(Invest.amount)).join(Project).filter(*f_fee_amount).scalar()
        if fee_amount is None:
            fee_amount = 0
        else:
            fee_amount = float(fee_amount) * 0.08
            fee_amount = round(fee_amount, 2)

        # - Aporte medio por cofinanciador(micromecenas)
        # OJO: En reporting.php no calcula esto mismo
        f_average_invest = list(filters)
        f_average_invest.append(Project.status.in_([4, 5, 6]))
        f_average_invest.append(Invest.status > 0)
        sub1 = db.session.query(func.avg(Invest.amount).label('amount')).join(Project)\
                                        .filter(*f_average_invest).group_by(Invest.user).subquery()
        average_invest = db.session.query(func.avg(sub1.c.amount)).scalar()
        average_invest = 0 if average_invest is None else round(average_invest, 2)

        # - Aporte medio por cofinanciador(micromecenas) mediante PayPal
        # OJO: En reporting.php no calcula esto mismo
        f_average_invest_paypal = list(f_average_invest)
        f_average_invest_paypal.append(Invest.method==Invest.METHOD_PAYPAL)
        sub1 = db.session.query(func.avg(Invest.amount).label('amount')).join(Project)\
                                        .filter(*f_average_invest_paypal).group_by(Invest.user).subquery()
        average_invest_paypal = db.session.query(func.avg(sub1.c.amount)).scalar()
        average_invest_paypal = 0 if average_invest_paypal is None else round(average_invest_paypal, 2)

        # - (Renombrar Coste mínimo medio por proyecto exitoso ] Presupuesto mínimo medio por proyecto exitoso
        # OJO: En reporting.php no calcula esto mismo
        f_average_mincost = list(filters2)
        f_average_mincost.append(Project.status.in_([4, 5]))
        average_mincost = db.session.query(func.avg(Project.minimum)).filter(*f_average_mincost).scalar()
        average_mincost = 0 if average_mincost is None else round(average_mincost, 2)

        # - Recaudación media por proyecto exitoso ( financiado )
        f_average_received = list(filters)
        f_average_received.append(Invest.status.in_([1, 3]))
        f_average_received.append(Project.status.in_([4, 5]))
        average_received = db.session.query(func.sum(Invest.amount) / func.count(func.distinct(Project.id)))\
                                    .join(Project).filter(*f_average_received).scalar()
        average_received = 0 if average_received is None else round(average_received, 2)

        # - Perc. medio de recaudación sobre el mínimo (número del dato anterior)
        f_comprometido_success = list(filters)
        f_comprometido_success.append(Invest.status.in_([1, 3]))
        f_comprometido_success.append(Project.status.in_([4, 5]))
        sub = db.session.query((func.sum(Invest.amount) / Project.minimum * 100 - 100).label('percent'))\
                            .select_from(Invest).join(Project)\
                            .filter(*f_comprometido_success).group_by(Invest.project).subquery()
        comprometido_success = db.session.query(func.avg(sub.c.percent)).scalar()
        comprometido_success = 0 if comprometido_success is None else round(comprometido_success, 2)
        # FIXME: - 100

        # (Nuevo) Dinero medio solo obtenido en 2a ronda
        f_average_second_round = list(filters)
        f_average_second_round.append(Invest.date_invested >= Project.date_passed)
        sub = db.session.query(func.sum(Invest.amount).label('amount')).join(Project)\
                                            .filter(*f_average_second_round).group_by(Project.id).subquery()
        average_second_round = db.session.query(func.avg(sub.c.amount)).scalar()
        average_second_round = 0 if average_second_round is None else round(average_second_round, 2)

        # - [Renombrar Dinero compr. medio en proyectos archivados] Dinero recaudado de media en campañas fallidas
        f_average_failed = list(filters)
        f_average_failed.append(Project.status == 6)
        f_average_failed.append(Invest.status.in_([0, 4]))
        average_failed = db.session.query(func.sum(Invest.amount) / func.count(func.distinct(Project.id)))\
                                        .join(Project).filter(*f_average_failed).scalar()
        average_failed = 0 if average_failed is None else round(average_failed, 2)

        # - [Renombrar]Perc. dinero compr. medio (dinero recaudado de media) sobre mínimo (número del dato anterior)
        # Perc. dinero compr. medio sobre mínimo',
        f_comprometido_fail = list(filters)
        f_comprometido_fail.append(Invest.status.in_([0, 4]))
        f_comprometido_fail.append(Project.status == 6)
        sub = db.session.query((func.sum(Invest.amount) / Project.minimum * 100).label('percent'))\
                            .select_from(Invest).join(Project)\
                            .filter(*f_comprometido_fail).group_by(Invest.project).subquery()
        comprometido_fail = db.session.query(func.avg(sub.c.percent)).scalar()
        comprometido_fail = 0 if comprometido_fail is None else round(comprometido_fail, 2)

        # No se pueden donar centimos no? Hacer enteros?
        res = {'comprometido': comprometido, 'devuelto': devuelto,
                'paypal-amount': paypal_amount, 'tpv-amount': tpv_amount, 'cash-amount': cash_amount,
                'call-amount': call_amount, 'average-invest': average_invest,
                'average-invest-paypal': average_invest_paypal, 'average-mincost': average_mincost,
                'average-received': average_received, 'comprometido-success': comprometido_success,
                'average-second-round': average_second_round, 'average-failed': average_failed,
                'comprometido-fail': comprometido_fail, 'fee-amount': fee_amount}
                # 'results-per-page': limit,
                #'projects': map(lambda i: [i[0], {'recaudado': i[1]}], comprometido),

        res['filters'] = {}
        for k, v in args.items():
            if v is not None:
                res['filters'][k] = v

        return jsonify(res)
        #return {'invests': map(lambda i: {i.investid: marshal(i, invest_fields)}, invests)}
