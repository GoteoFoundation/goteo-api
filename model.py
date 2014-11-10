from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
import config

# DB class
#app = Flask(__name__)
app = Flask(__name__, static_url_path="")
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URI
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG'] = True
db = SQLAlchemy(app)


# DB classess
class User(db.Model):
    __tablename__ = 'user'

    userid = db.Column('id', String(50), primary_key=True)
    name = db.Column('name', String(100))
    # email = db.Column('email', String(255))

    def __repr__(self):
        # FIX
        return '<User %s: %s>' % (self.username, self.email)


class Invest(db.Model):
    __tablename__ = 'invest'

    investid = db.Column('id', Integer, primary_key=True)
    user = db.Column('user', String(50))
    project = db.Column('project', String(50))
    status = db.Column('status', Integer)

    def __repr__(self):
        return '<Invest %d: %s>' % (self.investid, self.project)


class Project(db.Model):
    __tablename__ = 'project'

    projectid = db.Column('id', String(50), primary_key=True)
    name = db.Column('name', String(255))  # tinytext
    category = db.Column('category', String(50))
    minimum = db.Column('mincost', Integer)
    optimum = db.Column('maxcost', Integer)
    #subtitle = db.Column('subtitle', String(255))
    #status = db.Column('status', Integer)
    #created = db.Column('created', Date)
    #updated = db.Column('updated', Date)
    #published = db.Column('published', Date)
    # total_funding
    # active_date
    # rewards
    # platform

    def __repr__(self):
        return '<Project %s: %s>' % (self.projectid, self.name)
