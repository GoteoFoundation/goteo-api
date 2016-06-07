# -*- coding: utf-8 -*-

#from flask.ext.sqlalchemy import Pagination
from sqlalchemy import Integer, String, Text
from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import asc
from sqlalchemy.orm import relationship

from ..cacher import cacher
from ..base_resources import AbstractLang

from .. import db

class SupportLang(AbstractLang, db.Model):
    __tablename__ = 'support_lang'

    id = db.Column('id', Integer, db.ForeignKey('support.id'), primary_key=True)
    lang = db.Column('lang', String(2), primary_key=True)
    name = db.Column('support', Text)
    description = db.Column('description', Text)
    pending = db.Column('pending', Integer)
    Support = relationship('Support', back_populates='Translations')

    def __repr__(self):
        return '<SupportLang %s(%s): %r>' % (self.id, self.lang, self.name)


class Support(db.Model):
    __tablename__ = 'support'

    id = db.Column('id', Integer, primary_key=True)
    name = db.Column('support', Text)
    description = db.Column('description', Text)
    type = db.Column('type', String(50))
    project_id = db.Column('project', String(50), db.ForeignKey('project.id'))
    thread = db.Column('thread', Integer)
    Translations = relationship("SupportLang",
                                primaryjoin = "and_(Support.id==SupportLang.id, SupportLang.pending==0)",
                                back_populates="Support", lazy='joined') # Eager loading to allow catching

    def __repr__(self):
        return '<Support(%d) %s of project %s>' % (self.id, self.support, self.project_id)

    @hybrid_method
    @cacher
    def list_by_project(self, project_id, lang=None):
        """Get a list of valid supports (non-economic needs) for project"""
        try:
            filters = [self.project_id==project_id]
            if lang:
                filters.append(SupportLang.id==self.id)
                filters.append(SupportLang.lang==lang)
                return SupportLang.query.distinct().filter(*filters).order_by(asc(self.id)).all()

            return self.query.distinct().filter(*filters).order_by(asc(self.id)).all()
        except NoResultFound:
            return []
