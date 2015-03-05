# -*- coding: utf-8 -*-

import time

from flask.ext.restful import fields
from flask.ext.sqlalchemy import sqlalchemy
from flask_restful_swagger import swagger

from api import db
from api.models.call import Call
from api.models.project import Project, ProjectCategory
from api.models.invest import Invest, InvestNode
from api.models.location import Location, LocationItem
from api.decorators import ratelimit, requires_auth

from api.base_endpoint import BaseList, Response

func = sqlalchemy.func


@swagger.model
class MoneyResponse(Response):
    """MoneyResponse"""

    resource_fields = {
        "average-failed"         : fields.Float,
        "average-donation"       : fields.Float,
        "average-donation-paypal": fields.Float,
        "average-minimum"        : fields.Float,
        "average-received"       : fields.Float,
        "average-second-round"   : fields.Float,
        "matchfund-amount"       : fields.Integer,
        "matchfundpledge-amount" : fields.Integer,
        "cash-amount"            : fields.Integer,
        "pledged"                : fields.Integer,
        "pledged-failed"         : fields.Float,
        "pledged-successful"     : fields.Float,
        "refunded"               : fields.Integer,
        "fee-amount"             : fields.Float,
        "paypal-amount"          : fields.Integer,
        "creditcard-amount"      : fields.Integer
    }

    required = resource_fields.keys()


class MoneyAPI(BaseList):
    """Get Money Statistics"""

    @swagger.operation(
        notes='Money report',
        nickname='money',
        responseClass=MoneyResponse.__name__,
        parameters=BaseList.INPUT_FILTERS,
        responseMessages=BaseList.RESPONSE_MESSAGES
    )
    @requires_auth
    @ratelimit()
    def get(self):
        """Get the Money Report
        <a href="http://developers.goteo.org/doc/reports#money">developers.goteo.org/doc/reports#money</a>
        """
        time_start = time.time()

        #remove not used arguments
        args = self.parse_args(remove=('page','limit'))

        filters = []
        filter_mincost = []  # para average_mincost
        filter_call = []  # para call_pledged_amount
        if 'from_date' in args and args['from_date'] is not None:
            filters.append(Invest.project == Project.id)
            filters.append(Invest.date_invested >= args['from_date'])
            filter_mincost.append(Invest.date_invested >= args['from_date'])
            filter_mincost.append(Invest.project == Project.id)
            filter_mincost.append(InvestNode.invest_id == Invest.id)
            filter_call.append(Call.date_published >= args['from_date'])
        if 'to_date' in args and args['to_date'] is not None:
            filters.append(Invest.project == Project.id)
            filters.append(Invest.date_invested <= args['to_date'])
            filter_mincost.append(Invest.date_invested <= args['to_date'])
            filter_mincost.append(Invest.project == Project.id)
            filter_mincost.append(InvestNode.invest_id == Invest.id)
            filter_call.append(Call.date_published <= args['to_date'])
        if 'project' in args and args['project'] is not None:
            filters.append(Project.id.in_(args['project']))
            filter_mincost.append(Project.id.in_(args['project']))
            # no afecta a filter_call
        if 'node' in args and args['node'] is not None:
            filters.append(Invest.id == InvestNode.invest_id)
            filter_mincost.append(Project.id == InvestNode.project_id)
            filters.append(InvestNode.invest_node.in_(args['node']))
            filter_mincost.append(InvestNode.invest_node.in_(args['node']))
            # FIXME: Call.node?
        if 'category' in args and args['category'] is not None:
            #TODO: category debe ser un string? en ingles? o el id de categoria?
            # try:
            #     category_id = db.session.query(Category.id).filter(Category.name.in_(args['category'])).one()
            #     category_id = category_id[0]
            # except NoResultFound:
            #     return bad_request("Invalid category")

            filters.append(Invest.project == ProjectCategory.project)
            filters.append(ProjectCategory.category.in_(args['category']))
            filter_mincost.append(Invest.project == ProjectCategory.project)
            filter_mincost.append(ProjectCategory.category.in_(args['category']))
            # no afecta a filter_call
        if 'location' in args and args['location'] is not None:
            # subquery = Location.location_subquery(**args['location'])
            # Using Vincenty on code's side to query only one time the DB
            subquery = Location.location_ids(**args['location'])
            filters.append(LocationItem.id.in_(subquery))
            filters.append(Invest.user == LocationItem.item)
            filters.append(LocationItem.type == 'user')
            # no afecta a filter_mincost ni filter_call


        res = MoneyResponse(
            starttime = time_start,
            attributes = {
                # Dinero comprometido: Suma recaudada por la plataforma
                "pledged"                 : Invest.pledged_total(**args),
                # "pledged"                 : Project.pledged_total(**args),
                # Perc. medio de recaudación sobre el mínimo recaudado
                "pledged-successful"      : Invest.percent_pledged_successful(**args),
                # "pledged-successful"      : Project.percent_pledged_successful(**args),
                # Perc. dinero compr. medio sobre mínimo',
                "pledged-failed"          : Invest.percent_pledged_failed(**args),
                # "pledged-failed"          : Project.percent_pledged_failed(**args),
                # Dinero devuelto (en proyectos archivados)
                "refunded"                : Invest.refunded_total(**args),
                # "refunded"                : Project.refunded_total(**args),
                # Recaudado mediante PayPal
                # TODO: confirmar si hay que quitar devueltos
                "paypal-amount"           : Invest.pledged_total(method=Invest.METHOD_PAYPAL, **args),
                # Recaudado mediante TPV
                "creditcard-amount"       : Invest.pledged_total(method=Invest.METHOD_TPV, **args),
                # # Aportes manuales: recaudado mediante transferencia bancaria directa
                "cash-amount"             : Invest.pledged_total(method=Invest.METHOD_CASH, **args),
                #  Suma recaudada en Convocatorias (Capital riego distribuido + crowd)
                # SOLO CONVOCATORIA:
                # "matchfund-amount"        : Invest.pledged_total(method=Invest.METHOD_DROP, **args),
                # CONVOCATORIA y aportes individuales
                "matchfund-amount"        : Invest.pledged_total(is_call=True, **args),
                # Capital Riego de Goteo (fondos captados de instituciones y empresas destinados a la bolsa de Capital Riego https://goteo.org/service/resources)
                "matchfundpledge-amount"  : Call.pledged_total(**args),
                # Total 8% recaudado por Goteo
                "fee-amount"              : Invest.fee_total(**args),
                # Aporte medio por cofinanciador(micromecenas)
                # OJO: En reporting.php no calcula esto mismo
                "average-donation"        : Invest.average_donation(**args),
                # Aporte medio por cofinanciador(micromecenas) mediante PayPal
                # OJO: En reporting.php no calcula esto mismo
                "average-donation-paypal" : Invest.average_donation(method=Invest.METHOD_PAYPAL, **args),
                # Coste mínimo medio por proyecto exitoso: Presupuesto mínimo medio por proyecto exitoso
                # TODO: ¿parametro location?
                # OJO: En reporting.php no calcula esto mismo
                "average-minimum"         : Project.average_minimum(**args),
                # Recaudación media por proyecto exitoso ( financiado )
                "average-received"        : Project.average_total(status=[Project.STATUS_FUNDED, Project.STATUS_FULFILLED], **args),
                # (Nuevo) Dinero medio solo obtenido en 2a ronda
                "average-second-round"    : Invest.average_second_round(**args),
                # - [Renombrar Dinero compr. medio en proyectos archivados] Dinero recaudado de media en campañas fallidas
                "average-failed"          : Project.average_total(status=[Project.STATUS_UNFUNDED], **args),
                # - [Renombrar]Perc. dinero compr. medio (dinero recaudado de media) sobre mínimo (número del dato anterior)
            },
            filters = args.items()
        )

        return res.response(self.json)

