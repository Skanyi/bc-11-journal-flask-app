'''
Create a form that will be used to create journal Entries
'''
from flask_wtf import Form
from flask.ext.pagedown.fields import PageDownField
from wtforms import BooleanField, StringField, PasswordField, validators, SubmitField
from wtforms.validators import DataRequired

class JournalForm(Form):
    body = PageDownField('Body', [validators.Length(min=1, max=1500)])
    tags = StringField('Tags', [validators.Length(min=1, max=20)])
    submit = SubmitField("Create")

class SearchForm(Form):
    search = StringField('search', validators=[DataRequired()])
    submit = SubmitField("Submit")
