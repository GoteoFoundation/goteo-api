# -*- coding: utf-8 -*-

from sqlalchemy import func, Integer, String, Text
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.orm import aliased
from sqlalchemy import asc, and_, distinct

from ..helpers import svg_image_url, get_lang
from ..decorators import cacher

from .. import db


# License stuff
class LicenseLang(db.Model):
    __tablename__ = 'license_lang'

    id = db.Column('id', String(50), db.ForeignKey('license.id'), primary_key=True)
    lang = db.Column('lang', String(2), primary_key=True)
    name_lang = db.Column('name', String(100))
    description_lang = db.Column('description', Text)
    url_lang = db.Column('url', String(255))
    pending = db.Column('pending', Integer)

    def __repr__(self):
        return '<LicenseLang %s: %r>' % (self.id, self.name_lang)

# License stuff
class License(db.Model):
    __tablename__ = 'license'

    id = db.Column('id', String(50), primary_key=True)
    name = db.Column('name', String(100))
    description = db.Column('description', Text)
    url = db.Column('url', String(255))
    order = db.Column('order', Integer)

    def __repr__(self):
        return '<License %s: %r>' % (self.id, self.name)

    @hybrid_property
    def svg_url(self):
    	return svg_image_url(self.id + '.svg')

    #Filters for table license
    @hybrid_property
    def filters(self):
        return []

    # Getting filters for this model
    @hybrid_method
    def get_filters(self, **kwargs):

        from ..models.location import Location, LocationItem
        from ..models.reward import Reward
        from ..models.project import Project, ProjectCategory

        filters = self.filters
        # Join project table if filters
        for i in ('node', 'from_date', 'to_date', 'project', 'category', 'location'):
            if i in kwargs and kwargs[i] is not None:
                filters.append(Reward.license == self.id)
                filters.append(Project.id == Reward.project)
                filters.append(Project.status.in_(Project.PUBLISHED_PROJECTS))
        # Filters by goteo node
        if 'node' in kwargs and kwargs['node'] is not None:
            filters.append(Project.node.in_(kwargs['node']))
        # Filters by "from date"
        # counting license created after this date
        if 'from_date' in kwargs and kwargs['from_date'] is not None:
            filters.append(Project.published >= kwargs['from_date'])
        # Filters by "to date"
        # counting license created before this date
        if 'to_date' in kwargs and kwargs['to_date'] is not None:
            filters.append(Project.published <= kwargs['to_date'])
        # Filters by "project"
        # counting attached (invested or collaborated) to some project(s)
        if 'project' in kwargs and kwargs['project'] is not None:
            filters.append(Project.id.in_(kwargs['project']))
        # filter by license interests
        if 'category' in kwargs and kwargs['category'] is not None:
            filters.append(ProjectCategory.project == Reward.project)
            filters.append(ProjectCategory.category.in_(kwargs['category']))
        #Filter by location
        if 'location' in kwargs and kwargs['location'] is not None:
            filters.append(LocationItem.type == 'project')
            filters.append(LocationItem.item == Reward.project)
            filters.append(LocationItem.locable == True)
            subquery = Location.location_subquery(**kwargs['location'])
            filters.append(LocationItem.id.in_(subquery))

        return filters

    @hybrid_method
    @cacher
    def get(self, id):
        """Get a valid license form id"""
        try:
            filters = list(self.filters)
            filters.append(License.id == id)
            return self.query.filter(*filters).one()
        except NoResultFound:
            return None

    @hybrid_method
    @cacher
    def list(self, **kwargs):
        """Get a list of valid license"""
        try:
            filters = list(self.get_filters(**kwargs))

            # In case of requiring languages, a LEFT JOIN must be generated
            if 'lang' in kwargs and kwargs['lang'] is not None:
                joins = []
                langs = {}
                cols = [self.id,self.name,self.url,self.description]
                for l in kwargs['lang']:
                    langs[l] = aliased(LicenseLang)
                    cols.append(langs[l].name_lang.label('name_' + l))
                    cols.append(langs[l].description_lang.label('description_' + l))
                    cols.append(langs[l].url_lang.label('url_' + l))
                    # cols.append(langs[l])
                    joins.append((langs[l], and_(langs[l].id == self.id, langs[l].lang == l)))
                ret = []
                for u in db.session.query(*cols).distinct().outerjoin(*joins).filter(*filters).order_by(asc(self.order)):
                    u = u._asdict()
                    u['name'] = get_lang(u, 'name', kwargs['lang'])
                    u['description'] = get_lang(u, 'description', kwargs['lang'])
                    u['url'] = get_lang(u, 'url', kwargs['lang'])
                    ret.append(u)
                return ret

            # No need for languages by default
            return self.query.distinct().filter(*filters).order_by(asc(self.order)).all()

        except NoResultFound:
            return []

    @hybrid_method
    @cacher
    def total(self, **kwargs):
        """Returns the total number of valid license"""
        try:
            filters = list(self.get_filters(**kwargs))
            count = db.session.query(func.count(distinct(self.id))).filter(*filters).scalar()
            if count is None:
                count = 0
            return count
        except MultipleResultsFound:
            return 0

