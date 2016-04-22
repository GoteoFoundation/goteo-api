# -*- coding: utf-8 -*-

#from flask.ext.sqlalchemy import Pagination
from sqlalchemy import or_, asc, desc, and_, distinct, func, Integer, String, Text, Date, Float
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.orm import aliased, relationship

from ..helpers import image_url, utc_from_local, get_lang, objectview
from ..cacher import cacher
from ..base_resources import AbstractLang
from ..models.post import Post, Blog
from .. import db


class ProjectLang(AbstractLang, db.Model):
    __tablename__ = 'project_lang'

    id = db.Column('id', String(50), db.ForeignKey('project.id'), primary_key=True)
    lang = db.Column('lang', String(2), primary_key=True)
    # name = db.Column('name', String(100))
    subtitle = db.Column('subtitle', Text)
    description = db.Column('description', Text)
    motivation = db.Column('motivation', Text)
    about = db.Column('about', Text)
    related = db.Column('related', Text)
    reward = db.Column('reward', Text)
    keywords = db.Column('keywords', Text)
    video = db.Column('video', String(255))
    media = db.Column('media', String(255))
    pending = db.Column('pending', Integer)
    project = relationship('Project', back_populates='translations')

    def __repr__(self):
        return '<ProjectLang %s(%s): %r>' % (self.id, self.lang, self.subtitle)

class Project(db.Model):
    """
        Projects status
        ===============
        status = 0 : Non considered or rejected
        status = 1 : EDITING, considerations:
                     - DRAFT if it has an "ugly" id
                     - NEGOTIATION if it has a "nice" id (is coming from the status = 2). Meaning, "needs more work by the user"
                                   if it has the "updated" date set means "still needs more work"
                     with date updated set
        status = 2 : REVIEWING (has a "nice" id), considerations:
                     - REVIEW PENDING if it doesn't have the "updated" date set
                     - SECOND REVIEW PENDING if it has the "updated" date set (when it's coming from a second edition by the user)
        status = 3 : Published (hast the "updated" date set) during the 2 rounds
                     Funded if the has passed the first round
        status = 4 : Funded, after the 2 rounds only
        status = 5 : Fulfilled, after funded an editor can decide to put this status meaning "Outstanding project"
        status = 6 : Project failed after an unsuccessful campaign


        """
    __tablename__ = 'project'

    #PROJECT STATUS IDs
    STATUS_REJECTED    = 0
    STATUS_EDITING     = 1 #
    STATUS_REVIEWING   = 2 # reviewing
    STATUS_IN_CAMPAIGN = 3
    STATUS_FUNDED      = 4
    STATUS_FULFILLED   = 5 # 'Caso de exito'
    STATUS_UNFUNDED    = 6 # proyecto fallido
    STATUS_STR = ('rejected', 'editing', 'reviewing', 'in_campaign', 'funded', 'fulfilled', 'unfunded')

    RECEIVED_PROJECTS = [STATUS_REVIEWING, STATUS_IN_CAMPAIGN, STATUS_FUNDED, STATUS_FULFILLED, STATUS_UNFUNDED]
    PUBLISHED_PROJECTS = [STATUS_IN_CAMPAIGN, STATUS_FUNDED, STATUS_FULFILLED, STATUS_UNFUNDED]
    SUCCESSFUL_PROJECTS = [STATUS_IN_CAMPAIGN, STATUS_FUNDED, STATUS_FULFILLED]

    SCOPES_STR = ('', 'local', 'regional', 'national', 'global')

    id = db.Column('id', String(50), primary_key=True)
    owner = db.Column('owner', String(50), db.ForeignKey('user.id'))
    name = db.Column('name', Text)
    subtitle = db.Column('subtitle', Text)
    description = db.Column('description', Text)
    motivation = db.Column('motivation', Text)
    goal = db.Column('goal', Text)
    about = db.Column('about', Text)
    keywords = db.Column('keywords', Text)
    related = db.Column('related', Text)
    reward = db.Column('reward', Text)
    lang = db.Column('lang', String(2))
    currency = db.Column('currency', String(4))
    currency_rate = db.Column('currency_rate', Float)
    image = db.Column('image', String(255))
    video = db.Column('video', String(255))
    media = db.Column('media', String(255))
    minimum = db.Column('mincost', Integer)
    optimum = db.Column('maxcost', Integer)
    amount = db.Column('amount', Integer)
    status = db.Column('status', Integer) # estado del proyecto
    scope = db.Column('scope', Integer) #
    passed = db.Column('passed', Date) # fecha de paso de primera ronda
    created = db.Column('created', Date) # fecha de creacion
    updated = db.Column('updated', Date) # fecha de actualizacion de datos de formulario
    # deberia haber un campo como el updated solo hasta que se publica el proyecto,
    # luego coincidiria con el publicado
    published = db.Column('published', Date) # fecha de publicacion de proyecto
    closed = db.Column('closed', Date) # fecha de cierre de proyecto
    success = db.Column('success', Date) # fecha de éxito de proyecto
    node = db.Column('node', String(50), db.ForeignKey('node.id'))
    # total_funding
    # active_date
    # rewards
    # platform
    #aportes = db.relationship('Invest', backref='project')
    #
    translations = relationship("ProjectLang",
                                primaryjoin = "and_(Project.id==ProjectLang.id, ProjectLang.pending==0)",
                                back_populates="project", lazy='joined') # Eager loading to allow catching

    def __repr__(self):
        return '<Project %s: %s>' % (self.id, self.name)

    @hybrid_property
    def user(self):
        from ..users.models import User
        return User.get(self.owner)

    @hybrid_property
    def owner_name(self):
        return self.user.name

    @hybrid_property
    def image_url(self):
        return image_url(self.image, size="big")

    @hybrid_property
    def date_created(self):
        return utc_from_local(self.created)

    @hybrid_property
    def date_updated(self):
        return utc_from_local(self.updated)

    @hybrid_property
    def date_published(self):
        return utc_from_local(self.published)

    @hybrid_property
    def date_passed(self):
        return utc_from_local(self.passed)

    @hybrid_property
    def date_succeeded(self):
        return utc_from_local(self.success)

    @hybrid_property
    def date_closed(self):
        return utc_from_local(self.closed)

    @hybrid_property
    def status_string(self):
        return self.STATUS_STR[self.status]

    @hybrid_property
    def scope_string(self):
        if self.scope:
            return self.SCOPES_STR[self.scope]
        return self.SCOPES_STR[0]

    # Getting filters for this model
    @hybrid_method
    def get_filters(self, **kwargs):
        "Return filters to be used"
        from ..models.reward import Reward
        from ..location.models import ProjectLocation
        from ..calls.models import CallProject

        # Filters by default only published projects
        filters = []

        # custom filters by project status
        if 'received' in kwargs and kwargs['received'] is not None:
            # Any project with a "updated" date set is a RECEIVED project
            # overwrite the default published filters
            filters = [self.updated != None, self.updated != '0000-00-00']
            kwargs['status'] = self.RECEIVED_PROJECTS
        elif 'successful' in kwargs and kwargs['successful'] is not None:
            # successful projects (checked by passed date only)
            filters.append(self.passed != None)
            filters.append(self.passed != '0000-00-00')
        elif 'finished' in kwargs and kwargs['finished'] is not None:
            # successful projects (checked by status bit)
            kwargs['status'] = [self.STATUS_FUNDED, self.STATUS_FULFILLED]
            # filters.append(self.status > self.STATUS_REJECTED)
        elif 'closed' in kwargs and kwargs['closed'] is not None:
            # successful, and closed campaign projects
            and1 = and_(self.passed != None, self.passed != '0000-00-00')
            and2 = and_(self.closed != None, self.closed != '0000-00-00')
            filters.append(or_(and1, and2))
        elif 'failed' in kwargs and kwargs['failed'] is not None:
            #overwrite default status search
            kwargs['status'] = self.STATUS_UNFUNDED

        if 'status' in kwargs and kwargs['status'] is not None:
            if isinstance(kwargs['status'], (list, tuple)):
                filters.append(self.status.in_(kwargs['status']))
            else:
                filters.append(self.status == kwargs['status'])
        else:
            filters.append(self.status.in_(self.PUBLISHED_PROJECTS))

        # # Join project table if filters
        for i in ('license', 'license_type'):
            if i in kwargs and kwargs[i] is not None:
                filters.append(self.id == Reward.project)
        if 'license_type' in kwargs and kwargs['license_type'] is not None:
            filters.append(Reward.type == kwargs['license_type'])
        if 'license' in kwargs and kwargs['license'] is not None:
            filters.append(Reward.license.in_(kwargs['license']))

        if 'from_date' in kwargs and kwargs['from_date'] is not None:
            if 'received' in kwargs:
                #Look at the updated date on RECEIVED projects
                filters.append(self.updated >= kwargs['from_date'])
            elif 'successful' in kwargs or 'finished' in kwargs:
                #Look at the passed date on SUCCESFUL projects
                filters.append(self.passed >= kwargs['from_date'])
            elif 'closed' in kwargs:
                #Look at the closed date on SUCCESFUL-closed projects
                filters.append(self.closed >= kwargs['from_date'])
            elif 'failed' in kwargs:
                #Look at the closed date on FAILED projects
                filters.append(self.closed >= kwargs['from_date'])
            else:
                #Look at the published date on PUBLISHED projects
                filters.append(self.published >= kwargs['from_date'])

        if 'to_date' in kwargs and kwargs['to_date'] is not None:
            if 'received' in kwargs:
                filters.append(self.updated <= kwargs['to_date'])
            elif 'successful' in kwargs or 'finished' in kwargs:
                filters.append(self.passed <= kwargs['to_date'])
            elif 'closed' in kwargs:
                filters.append(self.closed <= kwargs['to_date'])
            elif 'failed' in kwargs:
                filters.append(self.closed <= kwargs['to_date'])
            else:
                filters.append(self.published <= kwargs['to_date'])

        if 'project' in kwargs and kwargs['project'] is not None:
            filters.append(self.id.in_(kwargs['project']))

        if 'node' in kwargs and kwargs['node'] is not None:
            filters.append(self.node.in_(kwargs['node']))

        if 'category' in kwargs and kwargs['category'] is not None:
            filters.append(self.id == ProjectCategory.project)
            filters.append(ProjectCategory.category.in_(kwargs['category']))

        if 'location' in kwargs and kwargs['location'] is not None:
            subquery = ProjectLocation.location_subquery(**kwargs['location'])
            filters.append(ProjectLocation.id == self.id)
            filters.append(ProjectLocation.id.in_(subquery))

        if 'call' in kwargs and kwargs['call'] is not None:
            filters.append(self.id == CallProject.project)
            if isinstance(kwargs['call'], (list, tuple)):
                filters.append(CallProject.call.in_(kwargs['call']))
            else:
                filters.append(CallProject.call == kwargs['call'])


        return filters


    @hybrid_method
    @cacher
    def get(self, project_id):
        """Get a valid project form id"""
        try:
            filters = self.get_filters()
            filters.append(self.id == project_id)
            return self.query.filter(*filters).one()
        except NoResultFound:
            return None

    @hybrid_method
    @cacher
    def list(self, **kwargs):
        """Get a list of valid projects"""
        try:
            limit = kwargs['limit'] if 'limit' in kwargs else 10
            page = kwargs['page'] if 'page' in kwargs else 0
            filters = self.get_filters(**kwargs)
            # In case of requiring languages, a LEFT JOIN must be generated
            if 'lang' in kwargs and kwargs['lang'] is not None:
                ret = []
                for u in ProjectLang.get_query(kwargs['lang']) \
                                 .filter(*filters).order_by(asc(self.created)) \
                                 .offset(page * limit).limit(limit):
                    ret.append(ProjectLang.get_translated_object(u._asdict(), kwargs['lang'], u.lang))
                return ret
            # No langs, normal query
            return self.query.distinct().filter(*filters) \
                                        .order_by(asc(self.created)) \
                                        .offset(page * limit).limit(limit).all()
        except NoResultFound:
            return []

    @hybrid_method
    @cacher
    def total(self, **kwargs):
        """Total number of projects"""
        try:
            filters = self.get_filters(**kwargs)
            total = db.session.query(func.count(distinct(self.id))).filter(*filters).scalar()
            if total is None:
                total = 0
            return total
        except MultipleResultsFound:
            return 0

    @hybrid_method
    @cacher
    def pledged_total(self, **kwargs):
        """Total amount of money (€) raised by Goteo"""
        try:
            filters = self.get_filters(**kwargs)
            total = db.session.query(func.sum(distinct(self.amount))).filter(*filters).scalar()
            if total is None:
                total = 0
            return total
        except MultipleResultsFound:
            return 0

    @hybrid_method
    @cacher
    def refunded_total(self, **kwargs):
        """Refunded money (€) on projects """
        try:
            filters = self.get_filters(**kwargs)
            total = db.session.query(func.sum(distinct(self.amount))).filter(*filters).scalar()
            if total is None:
                total = 0
            return total
        except MultipleResultsFound:
            return 0

    @hybrid_method
    @cacher
    def percent_pledged(self, **kwargs):
        """Percentage of money raised over the minimum on projects """
        filters = self.get_filters(**kwargs)
        total = db.session.query(func.avg(self.amount / self.minimum * 100)).filter(*filters).scalar()
        total = 0 if total is None else round(total, 2)
        return total

    @hybrid_method
    @cacher
    def average_minimum(self, **kwargs):
        """Average minimum cost (€) for projects (NOTE: this field is not affected by the location filter)"""
        filters = self.get_filters(**kwargs)
        total = db.session.query(func.avg(self.minimum)).filter(*filters).scalar()
        total = 0 if total is None else round(total, 2)
        return total

    @hybrid_method
    @cacher
    def average_total(self, **kwargs):
        """Average money raised (€) for projects"""
        print('AVERAGE TOTAL', kwargs)
        filters = self.get_filters(**kwargs)
        total = db.session.query(func.avg(self.amount)).filter(*filters).scalar()
        total = 0 if total is None else round(total, 2)
        return total

    @hybrid_method
    @cacher
    def average_posts(self, **kwargs):
        """Average number of posts by projects"""
        filters = self.get_filters(**kwargs)
        filters.append(Post.publish == 1)
        sq1 = db.session.query(func.count(self.id).label('posts')).select_from(Post) \
                            .join(Blog, and_(Blog.id == Post.blog, Blog.type == 'project')) \
                            .join(self, self.id == Blog.owner) \
                            .filter(*filters).group_by(Post.blog).subquery()
        total = db.session.query(func.avg(sq1.c.posts)).scalar()
        total = 0 if total is None else round(total, 2)
        return total

    @hybrid_method
    @cacher
    def collaborated_list(self, **kwargs):
        """Get a list of projects with more collaborations"""
        from ..models.message import Message
        limit = kwargs['limit'] if 'limit' in kwargs else 10
        page = kwargs['page'] if 'page' in kwargs else 0
        filters = self.get_filters(**kwargs)

        cols = [self.id,
                self.name,
                self.subtitle,
                self.image,
                self.media,
                self.published,
                func.count(Message.id).label('total')]

        if 'lang' in kwargs and kwargs['lang'] is not None:
            joins = []
            for l in kwargs['lang']:
                alias = aliased(ProjectLang)
                cols.append(alias.subtitle.label('subtitle_' + l))
                joins.append((alias, and_(alias.id == self.id, alias.lang == l)))
            query = db.session.query(*cols).outerjoin(*joins)
        else:
            query = db.session.query(*cols)

        ret = []
        for u in query.join(Message) \
                      .filter(*filters).group_by(Message.project) \
                      .order_by(desc('total')).offset(page * limit).limit(limit):
            u = u._asdict()
            if 'lang' in kwargs and kwargs['lang'] is not None:
                u['subtitle'] = get_lang(u, 'subtitle', kwargs['lang'])
            ret.append(objectview(u))

        return ret

        # try:
        #     return db.session.query(self.id.label('project'),
        #                        self.name,
        #                        self.subtitle,
        #                        self.image,
        #                        self.media,
        #                        self.published,
        #                        func.count(Message.id).label('total')).join(Message) \
        #                     .filter(*filters).group_by(Message.project) \
        #                     .order_by(desc('total')).offset(page * limit).limit(limit).all()
        # except NoResultFound:
        #     return []

    @hybrid_method
    @cacher
    def donated_list(self, **kwargs):
        """Get a list of projects with more donations (by individual contributions)"""

        from ..invests.models import Invest

        limit = kwargs['limit'] if 'limit' in kwargs else 10
        page = kwargs['page'] if 'page' in kwargs else 0
        filters = self.get_filters(**kwargs)
        filters.append(Invest.status.in_(Invest.VALID_INVESTS))
        cols = [self.id,
                self.name,
                self.subtitle,
                self.image,
                self.media,
                self.published,
                func.count(Invest.id).label('total')]

        if 'lang' in kwargs and kwargs['lang'] is not None:
            joins = []
            for l in kwargs['lang']:
                alias = aliased(ProjectLang)
                cols.append(alias.subtitle.label('subtitle_' + l))
                joins.append((alias, and_(alias.id == self.id, alias.lang == l)))
            query = db.session.query(*cols).outerjoin(*joins)
        else:
            query = db.session.query(*cols)

        ret = []
        for u in query.join(Invest) \
                      .filter(*filters).group_by(Invest.project) \
                      .order_by(desc('total')).offset(page * limit).limit(limit):
            u = u._asdict()
            if 'lang' in kwargs and kwargs['lang'] is not None:
                u['subtitle'] = get_lang(u, 'subtitle', kwargs['lang'])
            ret.append(objectview(u))

        return ret


        # try:
        #     return db.session.query(*cols).join(Invest) \
        #                     .filter(*filters).group_by(Invest.project) \
        #                     .order_by(desc('total')).offset(page * limit).limit(limit).all()

        # except NoResultFound:
        #     return []

    @hybrid_method
    @cacher
    def received_list(self, **kwargs):
        """Get a list of projects with more donations (by amount)"""

        from ..invests.models import Invest

        limit = kwargs['limit'] if 'limit' in kwargs else 10
        page = kwargs['page'] if 'page' in kwargs else 0
        filters = self.get_filters(**kwargs)
        cols = [self.id,
                self.name,
                self.subtitle,
                self.image,
                self.media,
                self.lang,
                self.published,
                func.sum(Invest.amount).label('amount')]
        filters.append(Invest.status.in_(Invest.VALID_INVESTS))

        if 'lang' in kwargs and kwargs['lang'] is not None:
            joins = []
            for l in kwargs['lang']:
                alias = aliased(ProjectLang)
                cols.append(alias.subtitle.label('subtitle_' + l))
                joins.append((alias, and_(alias.id == self.id, alias.lang == l)))
            query = db.session.query(*cols).outerjoin(*joins)
        else:
            query = db.session.query(*cols)

        ret = []
        for u in query.join(Invest) \
                      .filter(*filters).group_by(Invest.project) \
                      .order_by(desc('amount')).offset(page * limit).limit(limit):
            u = u._asdict()
            if 'lang' in kwargs and kwargs['lang'] is not None:
                u['subtitle'] = get_lang(u, 'subtitle', kwargs['lang'])
            ret.append(objectview(u))

        return ret


class ProjectCategory(db.Model):
    __tablename__ = 'project_category'

    project = db.Column('project', String(50), db.ForeignKey('project.id'), primary_key=True)
    category = db.Column('category', Integer, db.ForeignKey('category.id'), primary_key=True)

    def __repr__(self):
        return '<ProjectCategory %s-%s>' % (self.project, self.category)


class ProjectImage(db.Model):
    __tablename__ = 'project_image'

    project = db.Column('project', String(50), db.ForeignKey('project.id'), primary_key=True)
    image = db.Column('image', String(255), primary_key=True)
    section = db.Column('section', String(50))
    url = db.Column('url', Text)
    order = db.Column('order', Integer)

    def __repr__(self):
        return '<ProjectImage %s-%s>' % (self.project, self.image)

    @hybrid_method
    @cacher
    def get(self, id, section=''):
        """Get a valid Location Item from id"""
        try:
            if section is None:
                return self.query.get(id)
            return self.query.filter(self.project == id, self.section == section).order_by(asc(self.order)).all()
        except:
            pass
        return []
