from flask import Flask, request, render_template, flash, redirect, url_for
from flask_login import (LoginManager, login_required, login_user,
                         current_user, logout_user, UserMixin)
from functools import wraps
from flask import g, request, redirect, url_for
from app import SignUpForm, LoginForm, EditForm
from app import JournalForm, SearchForm
from .models import Journal, User
from app import app, session,lm

current_user_id = -1

@lm.user_loader
def user_loader(user_id):
    return session.query(User).get(user_id)

@app.before_request
def before_request():
    g.user = current_user

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def index():
    return render_template('index.html')

def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')


@app.route("/login", methods=['POST', 'GET'])
def login():
    '''Authenticate if the user info is correct and then log the user in or redirect
    or redirect them to the sign up pagedown
    '''
    error = None
    form = LoginForm(request.form)
    if form.validate():
        user = session.query(User).filter_by(email=form.email.data).first()
        global current_user_id
        current_user_id = user.id
        if form.email.data == form.email.data:
            return redirect(url_for('viewentries'))
    else:
        flash_errors(form)
        print("If you have no account, sign up")
    return render_template('login.html', form=form)


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    #session.add(user)
    #session.commit()
    logout_user()
    return render_template("index.html")


@app.route("/signup", methods=['POST', 'GET'])
def signup():
    '''
    Register a new user and add the data to the database
    '''
    form = SignUpForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.firstname.data, form.lastname.data, form.username.data, form.email.data,
                    form.password.data)
        session.add(user)
        session.commit()
        flash('Thanks for registering, Create you first Journal')
        return redirect(url_for('login'))
    else:
        flash_errors(form)
    return render_template('signup.html', form=form)


@app.route("/newjournal", methods=['POST', 'GET'])
@login_required
def newjournal():
    '''
    Creates a new journal that has only tags and tags
    '''
    form = JournalForm(request.form)
    if request.method == 'POST' and form.validate():
        new = Journal(form.body.data, form.tags.data, current_user_id)
        print ("User id: "+ str(current_user_id))
        session.add(new)
        session.commit()
        flash('Your Journal has been Created')
        return redirect("viewentries/")
    else:
        flash_errors(form)
    return render_template('newjournal.html', form = form)

@app.route("/viewentries/<id>", methods=['GET'])
@app.route("/viewentries/", methods=['GET'])
@login_required
def viewentries(id=None):
    '''
    Return all the list of journals created by the user
    '''

    entry_rows = None
    if id is not None:
        entry_rows = session.query(Journal).filter(Journal.id==id)
    else:
        entry_rows = session.query(Journal).filter_by(user_id=current_user_id)
    entries = []
    for entry in entry_rows:
        entries.append({
            "id": entry.id,
            "body": entry.body,
            "tags": entry.tags
        })
    # import pdb; pdb.set_trace()
    return render_template('viewentries.html', entries=entries)
@app.route("/edit/<id>", methods=['GET', 'POST'])
@login_required
def edit(id):
    # Get the journal ID from the GET Requests
    # Display a form with the necessary fields i.e. body & tags
    # User submits the form then you get the new values
    # Update the database table where the entry ID is equal to <id>
    journal = session.query(Journal).first()
    form = EditForm(obj= journal)
    if request.method == 'POST' and id == id:
        journal.body = form.body.data
        journal.tags = form.tags.data
        session.populate(journal)
        session.commit()
        flash('Your Journal has been edited')
        return redirect(url_for('viewentries', Journal.id == id))
    else:
        flash_errors(form)
    return render_template('edit.html', form=form)

@app.route('/search/', methods=['GET'])
@login_required
def search():
    pass
