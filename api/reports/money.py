# -*- coding: utf-8 -*-

import time

from flask.ext.restful import fields
from flask.ext.sqlalchemy import sqlalchemy
from flask_restful_swagger import swagger
from sqlalchemy.orm.exc import NoResultFound

from config import config

from api import db
from api.models.models import Call
from api.models.category import Category
from api.models.project import Project, ProjectCategory
from api.models.invest import Invest, InvestNode
from api.models.location import Location, LocationItem
from api.decorators import *

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
            filters.append(Invest.date_invested >= args['from_date'])
            filter_mincost.append(Invest.date_invested >= args['from_date'])
            filter_call.append(Call.date_published >= args['from_date'])
        if 'to_date' in args and args['to_date'] is not None:
            filters.append(Invest.date_invested <= args['to_date'])
            filter_mincost.append(Invest.date_invested <= args['to_date'])
            filter_call.append(Call.date_published <= args['to_date'])
        if 'project' in args and args['project'] is not None:
            filters.append(Invest.project.in_(args['project']))
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
                # Dinero devuelto (en proyectos archivados)
                "refunded"                : self._refunded(list(filters)),
                #- Recaudado mediante PayPal
                #FIXME: No quitamos los devueltos?
                "paypal-amount"           : self._paypal_amount(list(filters)),
                #- Recaudado mediante TPV
                #FIXME: No quitamos los devueltos?
                "creditcard-amount"       : self._tpv_amount(list(filters)),
                # Aportes manuales: recaudado mediante transferencia bancaria directa
                #FIXME: No quitamos los devueltos?
                "cash-amount"             : self._cash_amount(list(filters)),
                # - [NEW] Suma recaudada en Convocatorias (Capital riego distribuido + crowd)
                #FIXME: No quitamos los devueltos?
                "matchfund-amount"        : self._call_amount(list(filters)),
                # Capital Riego de Goteo (fondos captados de instituciones y empresas destinados a la bolsa de Capital Riego https://goteo.org/service/resources)
                "matchfundpledge-amount"  : self._call_pledged_amount(list(filter_call)),
                # Total 8% recaudado por Goteo
                "fee-amount"              : self._fee_amount(list(filters)),
                # Aporte medio por cofinanciador(micromecenas)
                # OJO: En reporting.php no calcula esto mismo
                "average-donation"        : self._average_donation(list(filters)),
                # Aporte medio por cofinanciador(micromecenas) mediante PayPal
                # OJO: En reporting.php no calcula esto mismo
                "average-donation-paypal" : self._average_donation_paypal(list(filters)),
                # Coste mínimo medio por proyecto exitoso: Presupuesto mínimo medio por proyecto exitoso
                # TODO: ¿parametro location?
                # OJO: En reporting.php no calcula esto mismo
                "average-minimum"         : self._average_mincost(list(filter_mincost)),
                # Recaudación media por proyecto exitoso ( financiado )
                "average-received"        : self._average_received(list(filters)),
                # Perc. medio de recaudación sobre el mínimo (número del dato anterior)
                "pledged-successful"      : self._pledged_success(list(filters)),
                # (Nuevo) Dinero medio solo obtenido en 2a ronda
                "average-second-round"    : self._average_second_round(list(filters)),
                # - [Renombrar Dinero compr. medio en proyectos archivados] Dinero recaudado de media en campañas fallidas
                "average-failed"          : self._average_failed(list(filters)),
                # - [Renombrar]Perc. dinero compr. medio (dinero recaudado de media) sobre mínimo (número del dato anterior)
                # Perc. dinero compr. medio sobre mínimo',
                "pledged-failed"          : self._pledged_fail(list(filters))
            },
            filters = args.items()
        )

        return res.response(self.json)


    def _refunded(self, f_refunded=[]):
        f_refunded.append(Invest.status==Invest.STATUS_RETURNED)
        devuelto = db.session.query(func.sum(Invest.amount)).filter(*f_refunded).scalar()
        if devuelto is None:
            devuelto = 0
        return devuelto

    def _paypal_amount(self, f_paypal_amount=[]):
        f_paypal_amount.append(Invest.method==Invest.METHOD_PAYPAL)
        paypal_amount = db.session.query(func.sum(Invest.amount)).filter(*f_paypal_amount).scalar()
        if paypal_amount is None:
            paypal_amount = 0
        return paypal_amount

    def _tpv_amount(self, f_tpv_amount=[]):
        f_tpv_amount.append(Invest.method==Invest.METHOD_TPV)
        tpv_amount = db.session.query(func.sum(Invest.amount)).filter(*f_tpv_amount).scalar()
        if tpv_amount is None:
            tpv_amount = 0
        return tpv_amount

    def _cash_amount(self, f_cash_amount=[]):
        f_cash_amount.append(Invest.method==Invest.METHOD_CASH)
        cash_amount = db.session.query(func.sum(Invest.amount)).filter(*f_cash_amount).scalar()
        if cash_amount is None:
            cash_amount = 0
        return cash_amount

    def _call_pledged_amount(self, f_call_pledged_amount=[]):
        f_call_pledged_amount.append(Call.status > Call.STATUS_REVIEWING)
        call_pledged_amount = db.session.query(func.sum(Call.amount)).filter(*f_call_pledged_amount).scalar()
        if call_pledged_amount is None:
            call_pledged_amount = 0
        return call_pledged_amount

    def _call_amount(self, f_call_amount=[]):
        f_call_amount.append(Invest.method==Invest.METHOD_DROP)
        f_call_amount.append(Invest.call != None)
        f_call_amount.append(Invest.status.in_([Invest.STATUS_CHARGED, Invest.STATUS_PAID]))
        call_amount = db.session.query(func.sum(Invest.amount)).filter(*f_call_amount).scalar()
        if call_amount is None:
            call_amount = 0
        return call_amount

    def _fee_amount(self, f_fee_amount=[]):
        #TODO: corregir para sumar valores project_account.fee
        f_fee_amount.append(Project.status.in_([Project.STATUS_FUNDED, Project.STATUS_FULFILLED]))
        f_fee_amount.append(Invest.status.in_([Invest.STATUS_CHARGED, Invest.STATUS_PAID]))
        fee_amount = db.session.query(func.sum(Invest.amount)).join(Project).filter(*f_fee_amount).scalar()
        if fee_amount is None:
            fee_amount = 0
        else:
            fee_amount = float(fee_amount) * 0.08
            fee_amount = round(fee_amount, 2)
        return fee_amount

    def _average_donation(self, f_average_invest=[]):
        f_average_invest.append(Project.status.in_([Project.STATUS_FUNDED,
                                                    Project.STATUS_FULFILLED,
                                                    Project.STATUS_UNFUNDED]))
        f_average_invest.append(Invest.status > Invest.STATUS_PENDING)
        sub1 = db.session.query(func.avg(Invest.amount).label('amount')).join(Project)\
                                .filter(*f_average_invest).group_by(Invest.user).subquery()
        average_invest = db.session.query(func.avg(sub1.c.amount)).scalar()
        average_invest = 0 if average_invest is None else round(average_invest, 2)
        return average_invest

    def _average_donation_paypal(self, f_average_donation_paypal=[]):
        f_average_donation_paypal.append(Project.status.in_([Project.STATUS_FUNDED,
                                                             Project.STATUS_FULFILLED,
                                                            Project.STATUS_UNFUNDED]))
        f_average_donation_paypal.append(Invest.status > Invest.STATUS_PENDING)
        f_average_donation_paypal.append(Invest.method==Invest.METHOD_PAYPAL)
        sub1 = db.session.query(func.avg(Invest.amount).label('amount')).join(Project)\
                                        .filter(*f_average_donation_paypal).group_by(Invest.user).subquery()
        average_donation_paypal = db.session.query(func.avg(sub1.c.amount)).scalar()
        average_donation_paypal = 0 if average_donation_paypal is None else round(average_donation_paypal, 2)
        return average_donation_paypal

    def _average_mincost(self, f_average_mincost=[]):
        f_average_mincost.append(Project.status.in_([Project.STATUS_FUNDED,
                                                     Project.STATUS_FULFILLED]))
        average_mincost = db.session.query(func.avg(Project.minimum)).filter(*f_average_mincost).scalar()
        average_mincost = 0 if average_mincost is None else round(average_mincost, 2)
        return average_mincost

    def _average_received(self, f_average_received=[]):
        f_average_received.append(Project.status.in_([Project.STATUS_FUNDED,
                                                      Project.STATUS_FULFILLED]))
        average_received = db.session.query(func.avg(Project.amount))\
                                     .filter(*f_average_received).scalar()
        average_received = 0 if average_received is None else round(average_received, 2)
        return average_received

    def _pledged_success(self, f_pledged_success=[]):
        # FIXME: - 100
        f_pledged_success.append(Project.status.in_([Project.STATUS_FUNDED,
                                                     Project.STATUS_FULFILLED]))
        sub = db.session.query((Project.amount / Project.minimum * 100 - 100).label('percent'))\
                            .filter(*f_pledged_success).subquery()
        comprometido_success = db.session.query(func.avg(sub.c.percent)).scalar()
        comprometido_success = 0 if comprometido_success is None else round(comprometido_success, 2)
        return comprometido_success

    def _average_second_round(self, f_average_second_round=[]):
        f_average_second_round.append(Invest.date_invested >= Project.date_passed)
        sub = db.session.query(func.sum(Invest.amount).label('amount')).join(Project)\
                                            .filter(*f_average_second_round).group_by(Project.id).subquery()
        average_second_round = db.session.query(func.avg(sub.c.amount)).scalar()
        average_second_round = 0 if average_second_round is None else round(average_second_round, 2)
        return average_second_round

    def _average_failed(self, f_average_failed=[]):
        f_average_failed.append(Project.status == Project.STATUS_UNFUNDED)
        average_failed = db.session.query(func.avg(Project.amount) )\
                                        .filter(*f_average_failed).scalar()
        average_failed = 0 if average_failed is None else round(average_failed, 2)
        return average_failed

    def _pledged_fail(self, f_pledged_fail=[]):
        f_pledged_fail.append(Project.status == Project.STATUS_UNFUNDED)
        sub = db.session.query((Project.amount / Project.minimum * 100).label('percent'))\
                            .filter(*f_pledged_fail).subquery()
        comprometido_fail = db.session.query(func.avg(sub.c.percent)).scalar()
        comprometido_fail = 0 if comprometido_fail is None else round(comprometido_fail, 2)
        return comprometido_fail
