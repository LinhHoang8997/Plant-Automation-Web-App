from flaskr import db
from flaskr import login_manager

import bcrypt
from flask_login import UserMixin

from flask_wtf import FlaskForm
from wtforms import StringField, validators


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=10, message=u'Little short for an email address?')])
    password = StringField('Password', [validators.Length(min=10, message=u'Little short for an email address?')])
    # accept_rules = BooleanField('I accept the site rules', [validators.InputRequired()])


class AppUser(UserMixin, db.Model):
    __tablename__ = 'AppUser'
    appuser_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password, bcrypt.gensalt(rounds=14))

    def check_password(self, password):
        return bcrypt.checkpw(password, self.password_hash)


@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve

    """
    # return AppUser.query.get(user_id)
    # Just using it for  now, cuz the database is not ready yet
    return AppUser.query.get(user_id)
