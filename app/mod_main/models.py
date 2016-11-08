from app import db
from passlib.hash import sha256_crypt
from flask.ext.login import UserMixin

class Base(db.Model):
    '''Creates a model that all the other table models willinherit
    '''
    __abstract__ = True
    date_created = db.Column(db.DateTime,  default=db.func.current_timestamp().op('AT TIME ZONE')('EAT'))
    updated_on = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.now().op('AT TIME ZONE')('EAT'))

class User(UserMixin, Base):
    '''
    Creates a table that will store all the user information during registration
    '''
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

    '''
    Instantiate every new Instance
    '''
    def __init__(self, firstname, lastname, username, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.email = email
        self.password = password

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % self.username

    def set_password(self):
        '''
        Genereates a password using passlib
        '''
        self.password = sha256_crypt.encrypt((str(form.password.data)))

    '''
    Create a relationship between the user table and journal table by username
    User.username == Journal.username
    '''

class Tag(Base):
    """ This table model will create a table for tags"""
    __tablename__ = 'tags'
    id = db.Column(db.Integer)
    tagname = db.Column(db.String(80), primary_key=True )

    def __init__(self, tagname):
        self.tagname = tagname

    def __repr__(self):
        return '<Tag %r>' % self.tagname

class Journal(Base):
    '''
    Creates a table model that will store all the journals of the users grouped by username
    Date, body, tags
    '''
    __tablename__ = 'journal'

    id = db.Column(db.Integer, primary_key=True)
    User.username = db.Column(db.String(50), nullable=False, unique=True)
    body = db.Column(db.String(1500), nullable=False)
    tags = db.Column(db.String(50), nullable=True)

    def __init__(self, title, body, tags, user_id):
        self.title = title
        self.body = body
        self.tags = tags

    def __repr__(self):
        return '<Journal %r>' % self.title
