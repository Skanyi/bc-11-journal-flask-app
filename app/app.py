from flask import Flask, request, render_template, flash, session, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
from flask_login import LoginManager
from mod_auth.forms import SignUpForm, LoginForm


app = Flask(__name__) # , template_folder='./app/templates')
db = SQLAlchemy(app) # Initiliazation of database
app.secret_key = "SDFSDFSDF"
# Configurations
#app.config.from_object('config')

lm = LoginManager()
lm.init_app(app)
lm.login_view = "users.login"

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/login/", methods=['POST', 'GET'])
def login():
    form = LoginForm(request.form)
    if form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user, form.remember_me.data)
        return redirect(url_for('hello'))
    return render_template('login.html', form=form)

@app.route("/signup", methods=['POST', 'GET'])
def signup():
    form = SignUpForm(request.form)
    if request.method == 'POST' and form.validate():
        user = models.User(form.firstname.data, form.lastname.data, form.username.data, form.email.data,
                    form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)
