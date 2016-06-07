# -*- coding: utf-8 -*-

#from flask.ext.sqlalchemy import Pagination
from sqlalchemy import Integer, String, Text, Boolean, Date
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import asc
from sqlalchemy.orm import relationship

from ..helpers import utc_from_local
from ..cacher import cacher
from ..base_resources import AbstractLang

from .. import db

class CostLang(AbstractLang, db.Model):
    __tablename__ = 'cost_lang'

    id = db.Column('id', Integer, db.ForeignKey('cost.id'), primary_key=True)
    lang = db.Column('lang', String(2), primary_key=True)
    name = db.Column('cost', Text)
    description = db.Column('description', Text)
    pending = db.Column('pending', Integer)
    Cost = relationship('Cost', back_populates='Translations')

    def __repr__(self):
        return '<CostLang %s(%s): %r>' % (self.id, self.lang, self.name)

class Cost(db.Model):
    __tablename__ = 'cost'

    id = db.Column('id', Integer, primary_key=True)
    name = db.Column('cost', Text)
    description = db.Column('description', Text)
    type = db.Column('type', String(50))
    project_id = db.Column('project', String(50), db.ForeignKey('project.id'))
    amount = db.Column('amount', Integer)
    required = db.Column('required', Boolean)
    from_date = db.Column('from', Date)
    to_date = db.Column('until', Date)
    Translations = relationship("CostLang",
                                primaryjoin = "and_(Cost.id==CostLang.id, CostLang.pending==0)",
                                back_populates="Cost", lazy='joined') # Eager loading to allow catching

    def __repr__(self):
        return '<Cost(%d) %s of project %s>' % (self.id, self.cost[:50], self.project_id)

    @hybrid_property
    def date_from(self):
        return utc_from_local(self.from_date)

    @hybrid_property
    def date_to(self):
        return utc_from_local(self.to_date)

    @hybrid_method
    @cacher
    def list_by_project(self, project_id, lang=None):
        """Get a list of valid costs for project"""
        try:
            filters = [self.project_id==project_id]
            if lang:
                filters.append(CostLang.id==self.id)
                filters.append(CostLang.lang==lang)
                return CostLang.query.distinct().filter(*filters).order_by(asc(self.from_date)).all()
            return self.query.distinct().filter(*filters).order_by(asc(self.from_date)).all()
        except NoResultFound:
            return []
