# -*- coding: utf-8 -*-
from flask import abort, jsonify
from flask.ext.restful import Resource, reqparse, fields, marshal

from model import app, db
from model import Project, Invest, Call

from flask.ext.sqlalchemy import sqlalchemy


invest_fields = {
    'id': fields.Integer,
    'user': fields.String,
    'project': fields.String,
    'status': fields.Integer,
    'amount': fields.Integer
}


class MoneyAPI(Resource):

    def __init__(self):
        super(MoneyAPI, self).__init__()

    def get(self):
        func = sqlalchemy.func
        limit = 10

        # -  [Renombrar dinero comprometido] Suma recaudada por la plataforma
        comprometido = db.session.query(Invest.project, func.sum(Invest.amount)).group_by(Invest.project).limit(limit).all()

        # TODO: ??
        recaudado = db.session.query(func.sum(Invest.amount)).scalar()

        # - Dinero devuelto (en proyectos archivados)
        devuelto = db.session.query(func.sum(Invest.amount)).filter(Project.id==Invest.project, Project.status==4).scalar()

        # Á- [(SUPRIMIR EN INFORME] Perc. del comprometido que se ha devuelto
        # TODO: no se hace?

        #- Recaudado mediante PayPal
        paypal = db.session.query(func.sum(Invest.amount)).filter(Invest.method==Invest.METHOD_PAYPAL).scalar()

        #- Recaudado mediante TPV
        tpv = db.session.query(func.sum(Invest.amount)).filter(Invest.method==Invest.METHOD_TPV).scalar()

        #cash = db.session.query(func.sum(Invest.amount)).filter(Invest.method==Invest.METHOD_CASH).scalar()

        # - [Renombrar aportes manuales] Recaudado mediante transferencia bancaria directa
        # TODO

        # - [Renombrar] Capital Riego de Goteo (fondos captados de instituciones y empresas destinados a la bolsa de Capital Riego https://goteo.org/service/resources)
        # TODO: Comprobar que es correcto. Quitar las convocatorias de prueba que hay en la BD!!
        call_amount = db.session.query(func.sum(Call.amount)).scalar()

        # - [NEW] Suma recaudada en Convocatorias (Capital riego distribuido + crowd)
        # TODO

        # - Total 8% recaudado por Goteo
        # TODO: Comprobar
        #fee = recaudado * 0.08

        # - Aporte medio por cofinanciador(micromecenas)
        # TODO

        # - Aporte medio por cofinanciador(micromecenas) mediante PayPal
        # TODO

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

        if comprometido is None:
            abort(404)

        return jsonify({'total': int(recaudado), 'devuelto': int(devuelto), 'limit-per-page': limit,
                        'paypal': paypal, 'tpv': tpv, # 'cash': cash,
                        'call_amount': call_amount,
                        'projects': map(lambda i: [i[0], {'recaudado': i[1]}], comprometido)})
