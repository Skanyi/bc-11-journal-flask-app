from flask import Flask, request, render_template, flash, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
from flask_login import LoginManager
from app.forms import SignUpForm, LoginForm, EditForm
from app.forms import JournalForm, SearchForm
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_wtf.csrf import CsrfProtect

app = Flask(__name__) # , template_folder='./app/templates')
app.config.from_object('config')
db = SQLAlchemy(app) # Initiliazation of database
CsrfProtect(app)

engine = create_engine('sqlite:///journal.db', echo = True) # create a database when called
Session = sessionmaker(bind=engine)
session = Session()
# import models


lm = LoginManager()
lm.init_app(app)
lm.login_view = "users.login"

from app import views, models
