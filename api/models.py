# -*- coding: utf-8 -*-

#from flask.ext.sqlalchemy import Pagination
from sqlalchemy import Integer, String, Text, Date, DateTime, Float

from api import db


# DB classes
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column('id', String(50), primary_key=True)
    name = db.Column('name', String(100))
    active = db.Column('active', Integer)
    hide = db.Column('hide', Integer)
    node = db.Column('node', String(50), db.ForeignKey('node.id'))
    # email = db.Column('email', String(255))

    def __repr__(self):
        return '<User %s: %s>' % (self.name, self.email)


class UserRole(db.Model):
    __tablename__ = 'user_role'

    user_id = db.Column('user_id', String(50), db.ForeignKey('user.id'), primary_key=True)
    role_id = db.Column('role_id', String(50), primary_key=True)
    node_id = db.Column('node_id', String(50), db.ForeignKey('node.id'))

    def __repr__(self):
        return '<UserRole %s: %s>' % (self.user_id, self.role_id)


class Invest(db.Model):
    __tablename__ = 'invest'

    METHOD_PAYPAL = 'paypal'
    METHOD_TPV    = 'tpv'
    METHOD_CASH   = 'cash'
    METHOD_DROP   = 'drop'

    #INVEST STATUS IDs
    STATUS_PROCESSING = -1
    STATUS_PENDING    = 0
    STATUS_CHARGED    = 1
    STATUS_CANCELED   = 2
    STATUS_PAID       = 3
    STATUS_RETURNED   = 4
    STATUS_RELOCATED  = 5

    id = db.Column('id', Integer, primary_key=True)
    user = db.Column('user', String(50), db.ForeignKey('user.id'))
    project = db.Column('project', String(50), db.ForeignKey('project.id'))
    status = db.Column('status', Integer)
    amount = db.Column('amount', Integer)
    method = db.Column('method', String(20))
    date_invested = db.Column('invested', Date)
    date_charged = db.Column('charged', Date)
    resign = db.Column('resign', Integer)
    call = db.Column('call', String(50))

    def __repr__(self):
        return '<Invest %d: %s (%d EUR)>' % (self.id, self.project, self.amount)


class Project(db.Model):
    __tablename__ = 'project'

    #PROJECT STATUS IDs
    STATUS_REJECTED    = 0
    STATUS_EDITING     = 1
    STATUS_REVIEWING   = 2
    STATUS_IN_CAMPAIGN = 3
    STATUS_FUNDED      = 4
    STATUS_FULLFILED   = 5 # 'Caso de exito'
    STATUS_UNFUNDED    = 6 # proyecto fallido

    id = db.Column('id', String(50), primary_key=True)
    owner = db.Column('owner', String(50), db.ForeignKey('user.id'))
    name = db.Column('name', Text)
    category = db.Column('category', String(50), db.ForeignKey('category.id'))
    minimum = db.Column('mincost', Integer)
    optimum = db.Column('maxcost', Integer)
    #subtitle = db.Column('subtitle', String(255))
    status = db.Column('status', Integer)
    #created = db.Column('created', Date)
    date_passed = db.Column('passed', Date)
    date_updated = db.Column('updated', Date)
    date_published = db.Column('published', Date)
    date_closed = db.Column('closed', Date)
    node = db.Column('node', String(50), db.ForeignKey('node.id'))
    # total_funding
    # active_date
    # rewards
    # platform
    #aportes = db.relationship('Invest', backref='project')

    def __repr__(self):
        return '<Project %s: %s>' % (self.id, self.name)


class Node(db.Model):
    __tablename__ = 'node'

    id = db.Column('id', String(50), primary_key=True)
    name = db.Column('name', String(256))
    active = db.Column('active', Integer)

    def __repr__(self):
        return '<Node(%d): %s>' % (self.id, self.name)


class Call(db.Model):
    __tablename__ = 'call'

    #CALL STATUS IDs
    STATUS_CANCELED   = 0
    STATUS_EDITING    = 1
    STATUS_REVIEWING  = 2
    STATUS_APPLYING   = 3
    STATUS_PUBLISHING = 4
    STATUS_COMPLETED  = 5
    STATUS_EXPIRED    = 6

    id = db.Column('id', String(50), primary_key=True)
    name = db.Column('name', Text)
    amount = db.Column('amount', Integer)
    owner = db.Column('owner', String(50))
    status = db.Column('status', Integer)
    date_published = db.Column('published', Date)

    def __repr__(self):
        return '<Call %s: %s>' % (self.id, self.name)


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column('id', Integer, primary_key=True)
    name = db.Column('name', Text)

    def __repr__(self):
        return '<Category %s>' % (self.name)


class ProjectCategory(db.Model):
    __tablename__ = 'project_category'

    project = db.Column('project', String(50), db.ForeignKey('project.id'), primary_key=True)
    category = db.Column('category', Integer, db.ForeignKey('category.id'), primary_key=True)

    def __repr__(self):
        return '<Category %s>' % (self.name)


class Blog(db.Model):
    __tablename__ = 'blog'

    id = db.Column('id', Integer, primary_key=True)
    type = db.Column('type', String(10))
    owner = db.Column('owner', String(50))
    active = db.Column('active', Integer)

    def __repr__(self):
        return '<Blog(%d) %s %s>' % (self.id, self.type, self.owner)


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column('id', Integer, primary_key=True)
    blog = db.Column('blog', Integer, db.ForeignKey('blog.id'))
    title = db.Column('title', Text)
    date_publish = db.Column('date', Date)
    author = db.Column('author', String(50), db.ForeignKey('user.id'))
    publish = db.Column('publish', Integer)

    def __repr__(self):
        return '<Post(%d) %s: %s>' % (self.id, self.blog, self.title[:50])


class Reward(db.Model):
    __tablename__ = 'reward'

    id = db.Column('id', Integer, primary_key=True)
    project = db.Column('project', String(50), db.ForeignKey('project.id'))
    reward = db.Column('reward', Text)
    type = db.Column('type', String(50))
    amount = db.Column('amount', Integer)
    icon = db.Column('icon', String(50))

    def __repr__(self):
        return '<Reward(%d) %s: %s>' % (self.id, self.project[:10], self.title[:50])


class InvestNode(db.Model):
    __tablename__ = 'invest_node'

    user_id = db.Column('user_id', String(50))
    user_node = db.Column('user_node', String(50))
    project_id = db.Column('project_id', String(50))
    project_node = db.Column('project_node', String(50))
    invest_id = db.Column('invest_id', Integer, db.ForeignKey('invest.id'), primary_key=True)
    invest_node = db.Column('invest_node', String(50))

    def __repr__(self):
        return '<Invest %d in node %s>' % (self.invest_id, self.invest_node)


class InvestReward(db.Model):
    __tablename__ = 'invest_reward'

    invest = db.Column('invest', Integer, db.ForeignKey('invest.id'), primary_key=True)
    reward = db.Column('reward', Integer, db.ForeignKey('reward.id'), primary_key=True)

    def __repr__(self):
        return '<Invest(%d) - Reward(%d)>' % (self.invest, self.reward)


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


class UserInterest(db.Model):
    __tablename__ = 'user_interest'

    user = db.Column('user', String(50), db.ForeignKey('user.id'), primary_key=True)
    interest = db.Column('interest', Integer, db.ForeignKey('category.id'), primary_key=True)

    def __repr__(self):
        return '<UserInterest from %s to project %s>' % (self.user, self.project)


class Cost(db.Model):
    __tablename__ = 'cost'

    id = db.Column('id', Integer, primary_key=True)
    cost = db.Column('cost', Text)
    description = db.Column('description', Text)
    type = db.Column('type', String(50))
    project = db.Column('project', String(50))
    amount = db.Column('amount', Integer)
    required = db.Column('required', Integer)

    def __repr__(self):
        return '<Cost(%d) %s of project %s>' % (self.id, self.cost[:50], self.project)


class Location(db.Model):
    __tablename__ = 'location'

    id = db.Column('id', Integer, primary_key=True)
    city = db.Column('city', String(255))
    region = db.Column('region', String(255))
    country = db.Column('country', String(255))
    country_code = db.Column('country_code', String(2))
    lon = db.Column('longitude', Float)
    lat = db.Column('latitude', Float)
    valid = db.Column('valid', Integer)
    modified = db.Column('modified', DateTime)

    def __repr__(self):
        return '<Location(%d) %s, %s (%s)>' % (self.id, self.city, self.region, self.country)


class LocationItem(db.Model):
    __tablename__ = 'location_item'

    id = db.Column('location', Integer)
    item = db.Column('item', String(50), primary_key=True)
    type = db.Column('type', String(7), primary_key=True)
    method = db.Column('method', String(50))
    locable = db.Column('locable', Integer)
    info = db.Column('info', String(255))
    modified = db.Column('modified', DateTime)

    def __repr__(self):
        return '<LocationItem: (%s)%s in location %d>' % (self.type, self.item, self.id)


class UserApi(db.Model):
    __tablename__ = 'user_api'

    user = db.Column('user_id', String(50), primary_key=True)
    key = db.Column('key', String(50))
    expiration_date = db.Column('expiration_date', DateTime)

    def __repr__(self):
        return '<UserApi: %s %s (%s)>' % (self.user, self.key, self.expiration_date)
