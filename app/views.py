from flask import Flask, request, render_template, flash, redirect, url_for
from app import SignUpForm, LoginForm, EditForm
from app import JournalForm, SearchForm
from .models import Journal, User
from app import app, session


@app.route("/index")
def index():
    return render_template('index.html')

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
            "id": entry.id,
            "body": entry.body,
            "tags": entry.tags
        })
    # import pdb; pdb.set_trace()
    return render_template('viewentries.html', entries=entries)
@app.route("/edit/<id>", methods=['GET', 'POST'])
#@login_required
def edit(id):
    # Get the journal ID from the GET Requests
    # Display a form with the necessary fields i.e. body & tags
    # User submits the form then you get the new values
    # Update the database table where the entry ID is equal to <id>
    journal = session.query(Journal).first()
    form = EditForm(obj= journal)
    if request.method == 'POST':
        journal.body = form.body.data
        journal.tags = form.tags.data
        session.add(journal)
        session.commit()
        flash('Your Journal has been edited')
        return redirect(url_for('viewentries'))
    else:
        flash_errors(form)
    return render_template('edit.html', form=form)

@app.route('/search/', methods=['GET'])
#@login_required
'''def search():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return redirect(url_for('search', text=session.query(Journal)))'''


        #journal_entry.user_id = current_user.id
