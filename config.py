'''
The file contains the configuration of the application
'''
import os
DEBUG = True # Enable development environment

#To get the dirname of the absolute path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'journal.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True
DATABASE_CONNECT_OPTIONS = {}
