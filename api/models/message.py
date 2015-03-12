# -*- coding: utf-8 -*-

#from flask.ext.sqlalchemy import Pagination
from sqlalchemy import and_, desc, func, Integer, String, DateTime
from sqlalchemy.ext.hybrid import hybrid_method
from api import db
from .project import Project, ProjectCategory
from .location import Location, LocationItem
from ..decorators import cacher

class Message(db.Model):
    __tablename__ = 'message'

    id = db.Column('id', Integer, primary_key=True)
    project = db.Column('project', String(50), db.ForeignKey('project.id'))
    user = db.Column('user', String(50), db.ForeignKey('user.id'))
    thread = db.Column('thread', Integer)
    blocked = db.Column('blocked', Integer)
    date = db.Column('date', DateTime)
    # message = db.Column('message', Text)

    def __repr__(self):
        return '<Message(%d) from %s to project %s>' % (self.id, self.user, self.project)

    # Getting filters for this model
    @hybrid_method
    def get_filters(self, **kwargs):
        filters = []
        if 'from_date' in kwargs and kwargs['from_date'] is not None:
            filters.append(self.date >= kwargs['from_date'])
        if 'to_date' in kwargs and kwargs['to_date'] is not None:
            filters.append(self.date <= kwargs['to_date'])
        if 'project' in kwargs and kwargs['project'] is not None:
            filters.append(self.project.in_(kwargs['project']))
        if 'node' in kwargs and kwargs['node'] is not None:
            from .user import User
            filters.append(self.user == User.id)
            filters.append(User.node.in_(kwargs['node']))
        if 'category' in kwargs and kwargs['category'] is not None:
            filters.append(self.project == ProjectCategory.project)
            filters.append(ProjectCategory.category.in_(kwargs['category']))
        if 'location' in kwargs and kwargs['location'] is not None:
            filters.append(self.user == LocationItem.item)
            filters.append(LocationItem.type == 'user')
            subquery = Location.location_subquery(**kwargs['location'])
            filters.append(LocationItem.id.in_(subquery))

        return filters

    @hybrid_method
    @cacher
    def collaborators_list(self, **kwargs):
        """Get a list of of collaborators"""
        from .user import User
        limit = kwargs['limit'] if 'limit' in kwargs else 10
        page = kwargs['page'] if 'page' in kwargs else 0
        filters = list(self.get_filters(**kwargs))
        filters.append(self.user == User.id)
        # Exclude threads initiated by owners
        filters.append(self.thread != None)
        res = db.session.query(Message.user, User.name, User.id, User.avatar, func.count(Message.id).label('interactions'))\
                        .filter(*filters).group_by(Message.user)\
                        .order_by(desc('interactions')).offset(page * limit).limit(limit)
        ret = []
        for u in res:
            u = u._asdict()
            ret.append(u)
        return ret

    @hybrid_method
    @cacher
    def collaborators_total(self, **kwargs):
        """Total number of collaborators"""
        filters = list(self.get_filters(**kwargs))
        res = db.session.query(func.count(func.distinct(self.user))).filter(*filters).scalar()
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
        filters.append(self.project != Project.id)
        res = db.session.query(func.count(func.distinct(self.user)))\
                                    .join(Project, and_(Project.owner == self.user, Project.status.in_([
                                        Project.STATUS_FUNDED,
                                        Project.STATUS_FULFILLED,
                                        Project.STATUS_IN_CAMPAIGN,
                                        Project.STATUS_UNFUNDED
                                    ])))\
                                    .filter(*filters).scalar()
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
        sq = db.session.query(func.count(func.distinct(Message.user)).label("co"))\
                                    .join(Project, Message.project == Project.id)\
                                    .filter(*filters).group_by(Message.project).subquery()
        res = db.session.query(func.avg(sq.c.co)).scalar()
        if res is None:
            res = 0
        return res

