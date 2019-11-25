import json
import os
from flaskr.definitions import ROOT_DIR
import urllib.parse

with open(os.path.join(ROOT_DIR, 'model/credentials.json')) as f:
    creds = json.load(f)  #don't put /, as that will count as absolute and overwrite the first path

class Config(object):
    username = creds['username']
    password_parsed = urllib.parse.quote_plus(creds['password'])
    hostname = '172.104.17.155:3306'
    db_name = 'plant_app_data'

    # SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{}:{}@{}/{}'.format(username, password_parsed, hostname, db_name)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}.db'.format(db_name)
    SQLALCHEMY_POOL_RECYCLE = 3600
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SEND_FILE_MAX_AGE_DEFAULT = 0
    SECRET_KEY = '3ebd6cb7f09051684dbc3f5927364e239236e2955d6c57bb'

