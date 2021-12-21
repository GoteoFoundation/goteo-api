# -*- coding: utf-8 -*-

from sqlalchemy import or_, asc, desc, and_, distinct
from sqlalchemy import func, Integer, String, Text, Date, Float
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.orm import aliased, relationship
from datetime import date

from ..helpers import image_url, project_url, project_widget_url,as_list
from ..helpers import utc_from_local, get_lang
from ..cacher import cacher
from ..base_resources import AbstractLang
from ..models.post import Post, Blog
from .. import db


class ProjectLang(AbstractLang, db.Model):
    __tablename__ = 'project_lang'

    id = db.Column('id', String(50),
                   db.ForeignKey('project.id'), primary_key=True)
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
    social_commitment_description = db.Column('social_commitment_description', Text)
    pending = db.Column('pending', Integer)
    Project = relationship('Project', back_populates='Translations')

    def __repr__(self):
        return '<ProjectLang %s(%s): %r>' % (
            self.id, self.lang, self.subtitle)

    @hybrid_property
    def description_short(self):
        return self.subtitle

class ProjectCategory(db.Model):
    __tablename__ = 'project_category'

    project_id = db.Column('project', String(50),
                           db.ForeignKey('project.id'), primary_key=True)
    category_id = db.Column('category', Integer,
                            db.ForeignKey('category.id'), primary_key=True)

    def __repr__(self):
        return '<ProjectCategory %s-%s>' % (self.project_id, self.category_id)

class ProjectConf(db.Model):
    __tablename__ = 'project_conf'

    project_id = db.Column('project', String(50),
                           db.ForeignKey('project.id'), primary_key=True)
    days_round1 = db.Column('days_round1', Integer)
    days_round2 = db.Column('days_round2', Integer)
    one_round = db.Column('one_round', Integer)

    def __repr__(self):
        return '<ProjectConf %s-%s>' % (self.project_id, self.days_round1, self.days_round2, self.one_round)

    @hybrid_method
    @cacher
    def get(self, project_id):
        """Get a valid project form id"""
        try:
            return self.query \
                       .filter(self.project_id == project_id).one()
        except NoResultFound:
            return None

class ProjectImage(db.Model):
    __tablename__ = 'project_image'

    project_id = db.Column('project', String(50),
                           db.ForeignKey('project.id'), primary_key=True)
    image = db.Column('image', String(255), primary_key=True)
    section = db.Column('section', String(50))
    url = db.Column('url', Text)
    order = db.Column('order', Integer)

    def __repr__(self):
        return '<ProjectImage %s-%s>' % (self.project_id, self.image)

    @hybrid_method
    @cacher
    def get(self, id, section=''):
        """Get a valid Location Item from id"""
        try:
            if section is None:
                return self.query.get(id)
            return self.query \
                .filter(self.project_id == id, self.section == section) \
                .order_by(asc(self.order)).all()
        except Exception:
            pass
        return []

class Project(db.Model):
    """
        Projects status
        ===============
        status = 0 : Non considered or rejected
        status = 1 : EDITING, considerations:
                     - DRAFT if it has an "ugly" id
                     - NEGOTIATION:
                        if it has a "nice" id:
                            (prior status was 2).
                            Meaning, "needs more work by the user"
                        if it has the "updated":
                            date set means "still needs more work"
                     with date updated set
        status = 2 : REVIEWING (has a "nice" id), considerations:
                     - REVIEW PENDING if it doesn't have the "updated" date set
                     - SECOND REVIEW PENDING if it has the "updated" date set
                        (when it's coming from a second edition by the user)
        status = 3 : Published (hast the "updated" date set)
                               during the 2 rounds
                     Funded if the has passed the first round
        status = 4 : Funded, after the 2 rounds only
        status = 5 : Fulfilled, after funded an editor can decide
                     to put this status meaning "Outstanding project"
        status = 6 : Project failed after an unsuccessful campaign

        """
    __tablename__ = 'project'

    # PROJECT STATUS IDs
    STATUS_REJECTED = 0
    STATUS_EDITING = 1  # editing
    STATUS_REVIEWING = 2  # reviewing
    STATUS_IN_CAMPAIGN = 3
    STATUS_FUNDED = 4
    STATUS_FULFILLED = 5  # 'Caso de exito'
    STATUS_UNFUNDED = 6  # proyecto fallido
    STATUS_STR = ('rejected',
                  'editing',
                  'reviewing',
                  'in_campaign',
                  'funded',
                  'fulfilled',
                  'unfunded')

    RECEIVED_PROJECTS = [STATUS_REJECTED,
                         STATUS_EDITING,
                         STATUS_REVIEWING,
                         STATUS_IN_CAMPAIGN,
                         STATUS_FUNDED,
                         STATUS_FULFILLED,
                         STATUS_UNFUNDED]
    PUBLISHED_PROJECTS = [STATUS_IN_CAMPAIGN,
                          STATUS_FUNDED,
                          STATUS_FULFILLED,
                          STATUS_UNFUNDED]
    SUCCESSFUL_PROJECTS = [STATUS_IN_CAMPAIGN,
                           STATUS_FUNDED,
                           STATUS_FULFILLED]

    SCOPES_STR = ('', 'local', 'regional', 'national', 'global')

    id = db.Column('id', String(50), primary_key=True)
    user_id = db.Column('owner', String(50), db.ForeignKey('user.id'))
    User = relationship("User", lazy='joined')  # Eager loading for catching
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
    status = db.Column('status', Integer)  # estado del proyecto
    scope = db.Column('scope', Integer)  #
    passed = db.Column('passed', Date)  # fecha de paso de primera ronda
    created = db.Column('created', Date)  # fecha de creacion
    # fecha de actualizacion de datos de formulario
    updated = db.Column('updated', Date)
    # fecha de publicacion de proyecto
    published = db.Column('published', Date)
    closed = db.Column('closed', Date)  # fecha de cierre de proyecto
    success = db.Column('success', Date)  # fecha de éxito de proyecto
    node_id = db.Column('node', String(50), db.ForeignKey('node.id'))

    social_commitment_description = db.Column('social_commitment_description', Text)
    social_commitment_id = db.Column('social_commitment', Integer, db.ForeignKey('social_commitment.id'))
    SocialCommitment = relationship("SocialCommitment", lazy='joined')  # Eager loading for catching
    ProjectConf = relationship("ProjectConf", lazy='joined')  # Eager loading for catching

    #
    Translations = relationship(
        "ProjectLang",
        primaryjoin="and_(Project.id==ProjectLang.id, ProjectLang.pending==0)",
        back_populates="Project", lazy='joined')  # Eager loading for catching

    def __repr__(self):
        return '<Project %s: %s>' % (self.id, self.name)

    @hybrid_property
    def social_commitment(self):
        from ..social_commitments.models import SocialCommitment
        return SocialCommitment.get(self.social_commitment_id, lang=self.lang)

    @hybrid_property
    def project_conf(self):
        return ProjectConf.get(self.id)

    @hybrid_method
    def status_number(self, status):
        """Returns apropiate numbers string statuses"""
        statuses = []
        for s in as_list(status):
            if s == 'all':
                return tuple(range(0, self.STATUS_UNFUNDED+1))
            if isinstance(s, str):
                statuses.append(self.STATUS_STR.index(s))
            else:
                statuses.append(s)
        return statuses

    @hybrid_property
    def node(self):
        return self.node_id

    @hybrid_property
    def owner(self):
        return self.user_id

    @hybrid_property
    def rounds(self):
        conf = self.project_conf
        one_round = conf.one_round if conf else 0
        days_round1 = conf.days_round1 if conf else 40
        days_round2 = conf.days_round2 if conf else 40
        days_passed = (date.today() - self.published).days
        remaining = remaining_round1 = days_round1 - days_passed
        remaining_round2 = 0
        if not one_round:
            remaining += days_round2  
            remaining_round2 = days_round2 if remaining_round1 > 0 else remaining  
        return { 
            "round1": days_round1,
            "round1-remaining": remaining_round1 if remaining_round1 > 0 else 0,
            "round2": 0 if one_round else days_round2,
            "round2-remaining": remaining_round2 if remaining_round2 > 0 else 0,
            "days-remaining": remaining if remaining > 0 else 0
        }

    @hybrid_property
    def owner_name(self):
        # Manually get the User object if not exists
        if not self.User:
            from ..users.models import User
            self.User = User.get(self.user_id)
        return self.User.name

    @hybrid_property
    def description_short(self):
        return self.subtitle

    @hybrid_property
    def image_url(self):
        return image_url(self.image, size="medium")

    @hybrid_property
    def image_url_big(self):
        return image_url(self.image, size="big")

    @hybrid_property
    def video_url(self):
        return self.media

    @hybrid_property
    def project_url(self):
        return project_url(self.id)

    @hybrid_property
    def widget_url(self):
        return project_widget_url(self.id)

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
        from ..invests.models import Invest
        from ..location.models import ProjectLocation
        from ..calls.models import CallProject
        from ..matchers.models import MatcherProject
        from ..sdgs.models import SdgSocialCommitment
        from ..footprints.models import FootprintSocialCommitment

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
            # overwrite default status search
            kwargs['status'] = self.STATUS_UNFUNDED

        statuses = self.PUBLISHED_PROJECTS
        if 'status' in kwargs and kwargs['status'] is not None:
            statuses = self.status_number(kwargs['status'])
        filters.append(self.status.in_(statuses))

        # # Join project table if filters
        for i in ('license', 'license_type'):
            if i in kwargs and kwargs[i] is not None:
                filters.append(self.id == Reward.project_id)
        if 'license_type' in kwargs and kwargs['license_type'] is not None:
            filters.append(Reward.type == kwargs['license_type'])
        if 'license' in kwargs and kwargs['license'] is not None:
            filters.append(Reward.license_id.in_(as_list(kwargs['license'])))

        if 'from_date' in kwargs and kwargs['from_date'] is not None:
            if 'received' in kwargs:
                # Look at the updated date on RECEIVED projects
                filters.append(self.updated >= kwargs['from_date'])
            elif 'successful' in kwargs or 'finished' in kwargs:
                # Look at the passed date on SUCCESFUL projects
                filters.append(self.passed >= kwargs['from_date'])
            elif 'closed' in kwargs:
                # Look at the closed date on SUCCESFUL-closed projects
                filters.append(self.closed >= kwargs['from_date'])
            elif 'failed' in kwargs:
                # Look at the closed date on FAILED projects
                filters.append(self.closed >= kwargs['from_date'])
            else:
                # Look at the published date on PUBLISHED projects
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

        # Search by owner
        if 'owner' in kwargs and kwargs['owner'] is not None:
            filters.append(self.user_id.in_(as_list(kwargs['owner'])))

        # Search by user invested in the project
        if 'user' in kwargs and kwargs['user'] is not None:
            filters.append(Invest.project_id == self.id)
            filters.append(Invest.status.in_(Invest.VALID_INVESTS))
            filters.append(Invest.user_id.in_(as_list(kwargs['user'])))
            # Filter by anonymous only has sense in case of user defined
            #  is_anonymous == False   => Not anonymous Invests
            #  is_anonymous == True   => Anonymous Invests
            #  is_anonymous == None  => all Invests
            if 'is_anonymous' in kwargs and kwargs['is_anonymous'] is not None:
                if kwargs['is_anonymous'] is True:
                    filters.append(Invest.anonymous == True)
                elif kwargs['is_anonymous'] is False:
                    filters.append(or_(Invest.anonymous == None,
                                       Invest.anonymous == False))

        if 'project' in kwargs and kwargs['project'] is not None:
            filters.append(self.id.in_(as_list(kwargs['project'])))

        if 'node' in kwargs and kwargs['node'] is not None:
            filters.append(self.node_id.in_(as_list(kwargs['node'])))

        if 'category' in kwargs and kwargs['category'] is not None:
            filters.append(self.id == ProjectCategory.project_id)
            filters.append(ProjectCategory.category_id.in_(as_list(kwargs['category'])))

        if 'social_commitment' in kwargs and kwargs['social_commitment'] is not None:
            filters.append(self.social_commitment_id.in_(as_list(kwargs['social_commitment'])))

        if 'sdg' in kwargs and kwargs['sdg'] is not None:
            sub1 = db.session.query(SdgSocialCommitment.social_commitment_id) \
                .filter(SdgSocialCommitment.sdg_id.in_(as_list(kwargs['sdg'])))
            filters.append(self.social_commitment_id.in_(sub1))
            # Search using categories but highly inefficient:
            # and1 = and_(self.social_commitment_id != None,
            #     self.social_commitment_id.in_(sub1))
            # sub2 = db.session.query(ProjectCategory.project_id) \
            #     .filter(ProjectCategory.project_id == SdgCategory.category_id, SdgCategory.sdg_id.in_(as_list(kwargs['sdg'])))
            # and2 = and_(self.social_commitment_id == None,
            #     self.id.in_(sub2))
            # filters.append(or_(and1, and2))

        if 'footprint' in kwargs and kwargs['footprint'] is not None:
            sub1 = db.session.query(FootprintSocialCommitment.social_commitment_id) \
                .filter(FootprintSocialCommitment.footprint_id.in_(as_list(kwargs['footprint'])))
            filters.append(self.social_commitment_id.in_(sub1))
            # Search using categories but highly inefficient:
            # and1 = and_(self.social_commitment_id != None,
            #     self.social_commitment_id.in_(sub1))
            # sub2 = db.session.query(ProjectCategory.project_id) \
            #     .filter(ProjectCategory.project_id == FootprintCategory.category_id, FootprintCategory.footprint_id.in_(as_list(kwargs['footprint'])))
            # and2 = and_(self.social_commitment_id == None,
            #     self.id.in_(sub2))
            # filters.append(or_(and1, and2))


        if 'loc_status' in kwargs and kwargs['loc_status'] is not None:
            if kwargs['loc_status'] == 'located':
                filters.append(self.id.in_(
                    db.session.query(ProjectLocation.id).subquery()))
            if kwargs['loc_status'] == 'unlocated':
                filters.append(~self.id.in_(
                    db.session.query(ProjectLocation.id).subquery()))

        if 'location' in kwargs and kwargs['location'] is not None:
            subquery = ProjectLocation.location_subquery(**kwargs['location'])
            filters.append(ProjectLocation.id == self.id)
            filters.append(ProjectLocation.id.in_(subquery))

        if 'call' in kwargs and kwargs['call'] is not None:
            filters.append(self.id == CallProject.project_id)
            filters.append(CallProject.call_id.in_(as_list(kwargs['call'])))

        if 'matcher' in kwargs and kwargs['matcher'] is not None:
            filters.append(self.id == MatcherProject.project_id)
            filters.append(MatcherProject.matcher_id.in_(as_list(kwargs['matcher'])))

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
                                    .filter(*filters) \
                                    .order_by(asc(self.created)) \
                                    .offset(page * limit) \
                                    .limit(limit):
                    ret.append(ProjectLang.get_translated_object(
                        u._asdict(),
                        kwargs['lang'],
                        u.lang))
                return ret
            # No langs, normal query
            return self.query.distinct().filter(*filters) \
                                        .order_by(asc(self.created)) \
                                        .offset(page * limit) \
                                        .limit(limit).all()
        except NoResultFound:
            return []

    @hybrid_method
    @cacher
    def total(self, **kwargs):
        """Total number of projects"""
        try:
            filters = self.get_filters(**kwargs)
            total = db.session.query(func.count(distinct(self.id))) \
                              .filter(*filters).scalar()
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
            total = db.session.query(func.sum(self.amount)) \
                              .filter(*filters).scalar()
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
            total = db.session.query(func.sum(self.amount)) \
                              .filter(*filters).scalar()
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
        total = db.session.query(func.avg(self.amount / self.minimum * 100)) \
                          .filter(*filters).scalar()
        total = 0 if total is None else round(total, 2)
        return total

    @hybrid_method
    @cacher
    def average_minimum(self, **kwargs):
        """Average minimum cost (€) for projects
        (NOTE: this field is not affected by the location filter)
        """
        filters = self.get_filters(**kwargs)
        total = db.session.query(func.avg(self.minimum)) \
                          .filter(*filters).scalar()
        total = 0 if total is None else round(total, 2)
        return total

    @hybrid_method
    @cacher
    def average_total(self, **kwargs):
        """Average money raised (€) for projects"""
        filters = self.get_filters(**kwargs)
        total = db.session.query(func.avg(self.amount)) \
                          .filter(*filters).scalar()
        total = 0 if total is None else round(total, 2)
        return total

    @hybrid_method
    @cacher
    def average_posts(self, **kwargs):
        """Average number of posts by projects"""
        filters = self.get_filters(**kwargs)
        filters.append(Post.publish == 1)
        sq1 = db.session.query(func.count(self.id).label('posts')) \
                        .select_from(Post) \
                        .join(Blog, and_(Blog.id == Post.blog_id,
                                         Blog.type == 'project')) \
                        .join(self, self.id == Blog.user_id) \
                        .filter(*filters).group_by(Post.blog_id) \
                        .subquery()
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
                self.lang,
                self.status,
                self.published,
                func.count(Message.id).label('total')]

        if 'lang' in kwargs and kwargs['lang'] is not None:
            joins = []
            for l in kwargs['lang']:
                alias = aliased(ProjectLang)
                cols.append(alias.subtitle.label('subtitle_' + l))
                joins.append((alias, and_(alias.id == self.id,
                                          alias.lang == l)))
            query = db.session.query(*cols).outerjoin(*joins)
        else:
            query = db.session.query(*cols)

        ret = []
        for u in query.join(Message) \
                      .filter(*filters).group_by(Message.project_id) \
                      .order_by(desc('total')) \
                      .offset(page * limit) \
                      .limit(limit):
            u = u._asdict()
            if 'lang' in kwargs and kwargs['lang'] is not None:
                u['subtitle'] = get_lang(u, 'subtitle', kwargs['lang'])
                for l in kwargs['lang']:
                    u.pop('subtitle_' + l)
            # Return an instance of the Project class
            ret.append(self(**u))

        return ret

    @hybrid_method
    @cacher
    def donated_list(self, **kwargs):
        """Get a list of projects with more donations
        (by individual contributions)
        """

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
                self.lang,
                self.status,
                self.published,
                func.count(Invest.id).label('total')]

        if 'lang' in kwargs and kwargs['lang'] is not None:
            joins = []
            for l in kwargs['lang']:
                alias = aliased(ProjectLang)
                cols.append(alias.subtitle.label('subtitle_' + l))
                joins.append((alias, and_(alias.id == self.id,
                                          alias.lang == l)))
            query = db.session.query(*cols).outerjoin(*joins)
        else:
            query = db.session.query(*cols)

        ret = []
        for u in query.join(Invest) \
                      .filter(*filters).group_by(Invest.project_id) \
                      .order_by(desc('total')) \
                      .offset(page * limit) \
                      .limit(limit):
            u = u._asdict()
            if 'lang' in kwargs and kwargs['lang'] is not None:
                u['subtitle'] = get_lang(u, 'subtitle', kwargs['lang'])
                for l in kwargs['lang']:
                    u.pop('subtitle_' + l)
            # Return an instance of the Project class
            ret.append(self(**u))

        return ret

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
                self.status,
                self.published,
                func.sum(Invest.amount).label('amount')]
        filters.append(Invest.status.in_(Invest.VALID_INVESTS))

        if 'lang' in kwargs and kwargs['lang'] is not None:
            joins = []
            for l in kwargs['lang']:
                alias = aliased(ProjectLang)
                cols.append(alias.subtitle.label('subtitle_' + l))
                joins.append((alias, and_(alias.id == self.id,
                                          alias.lang == l)))
            query = db.session.query(*cols).outerjoin(*joins)
        else:
            query = db.session.query(*cols)

        ret = []
        for u in query.join(Invest) \
                      .filter(*filters).group_by(Invest.project_id) \
                      .order_by(desc('amount')) \
                      .offset(page * limit) \
                      .limit(limit):
            u = u._asdict()
            if 'lang' in kwargs and kwargs['lang'] is not None:
                u['subtitle'] = get_lang(u, 'subtitle', kwargs['lang'])
                for l in kwargs['lang']:
                    u.pop('subtitle_' + l)
            # Return an instance of the Project class
            ret.append(self(**u))

        return ret

