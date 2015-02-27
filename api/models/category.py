# -*- coding: utf-8 -*-

from sqlalchemy import func, Integer, String, Text, Date
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from api.helpers import image_url
from sqlalchemy import asc, and_, or_, distinct
from sqlalchemy.orm import aliased

from api import db
from api.helpers import get_lang

from api.models.location import Location, LocationItem

# Category stuff

class CategoryLang(db.Model):
    __tablename__ = 'category_lang'

    id = db.Column('id', String(50), db.ForeignKey('category.id'), primary_key=True)
    lang = db.Column('lang', String(2), primary_key=True)
    category_lang = db.Column('name', Text)
    description_lang = db.Column('description', Text)
    pending = db.Column('pending', Integer)

    def __repr__(self):
        return '<CategoryLang %s: %r>' % (self.id, self.category_lang)

class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column('id', Integer, primary_key=True)
    category = db.Column('name', Text)
    description = db.Column('description', Text)
    order = db.Column('order', Integer)

    def __repr__(self):
        return '<Category %s: %r>' % (self.id, self.category)

    #Filters for table category
    @hybrid_property
    def filters(self):
        return [self.category != '']

    # Getting filters for this model
    @hybrid_method
    def get_filters(self, **kwargs):
        filters = self.filters
        # Filters by goteo node
        if 'node' in kwargs and kwargs['node'] is not None:
            # filters.append(Category.node.in_(kwargs['node']))
            pass
        # Filters by "from date"
        # counting category created after this date
        if 'from_date' in kwargs and kwargs['from_date'] is not None:
            # filters.append(Category.created >= kwargs['from_date'])
            pass
        # Filters by "to date"
        # counting category created before this date
        if 'to_date' in kwargs and kwargs['to_date'] is not None:
            # filters.append(Category.created <= kwargs['to_date'])
            pass
        # Filters by "project"
        # counting attached (invested or collaborated) to some project(s)
        if 'project' in kwargs and kwargs['project'] is not None:
        	pass
        # filter by category interests
        if 'category' in kwargs and kwargs['category'] is not None:
            pass
        #Filter by location
        if 'location' in kwargs and kwargs['location'] is not None:
            pass
        #TODO: more filters, like creators, invested, etc
        return filters

    @hybrid_method
    def get(self, id):
        """Get a valid category form id"""
        try:
            filters = list(self.filters)
            filters.append(Category.id == id)
            return self.query.filter(*filters).one()
        except NoResultFound:
            return None

    @hybrid_method
    def list(self, **kwargs):
        """Get a list of valid category"""
        try:
            filters = list(self.get_filters(**kwargs))
            # In case of requiring languages, a LEFT JOIN must be generated
            if 'lang' in kwargs and kwargs['lang'] is not None:
                joins = []
                langs = {}
                cols = [self.id,self.category,self.description]
                for l in kwargs['lang']:
                    langs[l] = aliased(CategoryLang)
                    cols.append(langs[l].category_lang.label('category_' + l))
                    cols.append(langs[l].description_lang.label('description_' + l))
                    joins.append((langs[l], and_(langs[l].id == self.id, langs[l].lang == l)))
                ret = []
                for u in db.session.query(*cols).outerjoin(*joins).filter(*filters).order_by(asc(self.order)):
                    u = u._asdict()
                    u['category'] = get_lang(u, 'category', kwargs['lang'])
                    u['description'] = get_lang(u, 'description', kwargs['lang'])
                    ret.append(u)
                return ret

            return self.query.filter(*filters).order_by(asc(self.order)).all()
        except NoResultFound:
            return []

    @hybrid_method
    def total(self, **kwargs):
        """Returns the total number of valid category"""
        try:
            filters = list(self.get_filters(**kwargs))
            count = db.session.query(func.count(distinct(self.id))).filter(*filters).scalar()
            if count is None:
                count = 0
            return count
        except MultipleResultsFound:
            return 0