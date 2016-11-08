'''
Create a form that will be used to create journal Entries
'''
from wtforms import Form, BooleanField, StringField, PasswordField, validators

class JournalForm(Form):
    body = StringField('firstname', [validators.Length(min=100, max=1500)])
    tags = StringField('firstname', [validators.Length(min=12, max=20)])


    
