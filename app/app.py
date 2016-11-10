from flask import Flask, request, render_template, flash, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
from flask_login import LoginManager
from mod_auth.forms import SignUpForm, LoginForm
from mod_main.forms import JournalForm, SearchForm
from mod_auth import forms
from sqlalchemy import create_engine
import config
from sqlalchemy.orm import sessionmaker
from flask_wtf.csrf import CsrfProtect

app = Flask(__name__) # , template_folder='./app/templates')
app.config.from_object(config)
db = SQLAlchemy(app) # Initiliazation of database
CsrfProtect(app)

engine = create_engine('sqlite:///journal.db', echo = True) # create a database when called
Session = sessionmaker(bind=engine)
session = Session()
# import models
from models import *

lm = LoginManager()
lm.init_app(app)
lm.login_view = "users.login"

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm(request.form)
    if form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user, form.remember_me.data)
        return redirect(url_for('hello'))
    return render_template('login.html', form=form)

def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')

@app.route("/signup", methods=['POST', 'GET'])
def signup():
    form = SignUpForm(request.form)
    if request.method == 'POST' and form.validate():
        user = models.User(form.firstname.data, form.lastname.data, form.username.data, form.email.data,
                    form.password.data)
        session.add(user)
        session.commit()
        flash('Thanks for registering')
        return redirect(url_for('login'))
    else:
        flash_errors(form)
    return render_template('signup.html', form=form)

@app.route("/newjournal", methods=['POST', 'GET'])
#@login_required
def newjournal():
    form = JournalForm(request.form)
    if request.method == 'POST' and form.validate():
        new = models.Journal(form.body.data, form.tags.data)
        session.add(new)
        session.commit()
        flash('Your Journal has been Created')
        return redirect(url_for('hello'))
    else:
        flash_errors(form)
    return render_template('newjournal.html', form = form)

@app.route("/viewentries", methods=['GET'])
#@login_required
def viewentries():
    entries = Journal.query.filter_by(User.id == Journal.jour_id)
    return render_template('viewentries.html')

if __name__ == "__main__":
    app.run(debug=True)
