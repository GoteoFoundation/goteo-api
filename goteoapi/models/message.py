# -*- coding: utf-8 -*-

from sqlalchemy import and_, desc, func, Integer, String, DateTime
from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy.orm.exc import NoResultFound

from ..projects.models import Project, ProjectCategory
from ..cacher import cacher

from .. import db


class Message(db.Model):
    __tablename__ = 'message'

    id = db.Column('id', Integer, primary_key=True)
    project_id = db.Column('project', String(50), db.ForeignKey('project.id'))
    user_id = db.Column('user', String(50), db.ForeignKey('user.id'))
    thread = db.Column('thread', Integer)
    blocked = db.Column('blocked', Integer)
    date = db.Column('date', DateTime)
    # message = db.Column('message', Text)

    def __repr__(self):
        return '<Message(%d) from %s to project %s>' % (self.id, self.user_id, self.project_id)

    # Getting filters for this model
    @hybrid_method
    def get_filters(self, **kwargs):
        from ..users.models import User
        from ..location.models import UserLocation

        filters = []
        if 'from_date' in kwargs and kwargs['from_date'] is not None:
            filters.append(self.date >= kwargs['from_date'])
        if 'to_date' in kwargs and kwargs['to_date'] is not None:
            filters.append(self.date <= kwargs['to_date'])
        if 'project' in kwargs and kwargs['project'] is not None:
            filters.append(self.project_id.in_(kwargs['project']))
        if 'node' in kwargs and kwargs['node'] is not None:
            filters.append(self.user_id == User.id)
            filters.append(User.node_id.in_(kwargs['node']))
        if 'category' in kwargs and kwargs['category'] is not None:
            filters.append(self.project_id == ProjectCategory.project_id)
            filters.append(ProjectCategory.category_id.in_(kwargs['category']))
        if 'location' in kwargs and kwargs['location'] is not None:
            filters.append(self.user_id == UserLocation.id)
            subquery = UserLocation.location_subquery(**kwargs['location'])
            filters.append(UserLocation.id.in_(subquery))

        # Search by owner
        if 'user' in kwargs and kwargs['user'] is not None:
            if isinstance(kwargs['user'], (list, tuple)):
                filters.append(self.user_id.in_(kwargs['user']))
            else:
                filters.append(self.user_id == kwargs['user'])

        return filters

    # excluir owners y admins
    @hybrid_method
    @cacher
    def collaborators_list(self, **kwargs):
        """Get a list of of collaborators"""
        from ..users.models import User

        limit = kwargs['limit'] if 'limit' in kwargs else 10
        page = kwargs['page'] if 'page' in kwargs else 0
        filters = list(self.get_filters(**kwargs))
        filters.append(self.user_id == User.id)
        # Exclude threads initiated by owners
        filters.append(self.thread != None)
        try:
            return db.session.query(self.user_id, User.name, User.id, User.avatar,
                                    func.count(self.id).label('interactions')) \
                             .filter(*filters).group_by(self.user_id) \
                             .order_by(desc('interactions')) \
                             .offset(page * limit).limit(limit).all()
        except NoResultFound:
            return []

    @hybrid_method
    @cacher
    def collaborators_total(self, **kwargs):
        """Total number of collaborators"""
        filters = list(self.get_filters(**kwargs))
        res = db.session.query(func.count(func.distinct(self.user_id))).filter(*filters).scalar()
        if res is None:
            res = 0
        return res

    @hybrid_method
    @cacher
    def projects_total(self, **kwargs):
        """Total number of projects"""
        filters = list(self.get_filters(**kwargs))
        res = db.session.query(func.count(func.distinct(self.project_id))).filter(*filters).scalar()
        if res is None:
            res = 0
        return res

    @hybrid_method
    @cacher
    def collaborators_creators_total(self, **kwargs):
        """Total number of collaborators who are also creators of some projects"""
        filters = list(self.get_filters(**kwargs))
        sq_blocked = db.session.query(self.id).filter(self.blocked == 1).subquery()
        filters.append(self.thread > 0)
        filters.append(self.thread.in_(sq_blocked))
        filters.append(self.project_id != Project.id)
        res = db.session.query(func.count(func.distinct(self.user_id))) \
                        .join(Project, and_(Project.user_id == self.user_id,
                              Project.status.in_([
                                Project.STATUS_FUNDED,
                                Project.STATUS_FULFILLED,
                                Project.STATUS_IN_CAMPAIGN,
                                Project.STATUS_UNFUNDED
                                ])
                              )) \
                        .filter(*filters) \
                        .scalar()
        if res is None:
            res = 0
        return res

    @hybrid_method
    @cacher
    def average_collaborators(self, **kwargs):
        """Average number of collaborators"""
        filters = list(self.get_filters(**kwargs))
        filters.append(Project.status.in_([Project.STATUS_FUNDED,
                                           Project.STATUS_FULFILLED]))
        sq = db.session.query(func.count(func.distinct(self.user_id)).label("co")) \
                       .join(Project, self.project_id == Project.id) \
                       .filter(*filters) \
                       .group_by(self.project_id) \
                       .subquery()
        res = db.session.query(func.avg(sq.c.co)).scalar()
        if res is None:
            res = 0
        return res
