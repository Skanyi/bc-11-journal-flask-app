'''
Create the form that will be used for registration and login in
'''
from flask_wtf import Form
from wtforms import BooleanField, StringField, PasswordField, validators, SubmitField

class LoginForm(Form):
    email = StringField('Email address', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired(message='Must provide a password.')])
    remember_me = BooleanField('remember_me', default=False)
    submit = SubmitField('Submit')



class SignUpForm(Form):
    firstname = StringField('firstname', [validators.Length(min=12, max=20)])
    lastname = StringField('firstname', [validators.Length(min=12, max=20)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])
    submit = SubmitField('Submit')

    '''def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False'''
