from flask import Flask, request, render_template, flash, redirect, url_for
from app import SignUpForm, LoginForm
from app import JournalForm, SearchForm
from .models import Journal, User
from app import app, session


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
        user = User(form.firstname.data, form.lastname.data, form.username.data, form.email.data,
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
        new = Journal(form.body.data, form.tags.data)
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
    # entries = session.query(Journal).filter(User.id == Journal.jour_id).all()
    entry_rows = session.query(Journal).all()
    entries = []
    for entry in entry_rows:
        entries.append({
            "body": entry.body,
            "tags": entry.tags
        })
    # import pdb; pdb.set_trace()
    return render_template('viewentries.html', entries=entries)
