from flaskr import db
from flaskr import login_manager

import bcrypt
from flask_login import UserMixin

from flask_wtf import FlaskForm
from wtforms import StringField, validators

from datetime import date

class LoginForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=10, message=u'Little short for an email address?')])
    password = StringField('Password', [validators.Length(min=10, message=u'Little short for an email address?')])
    # accept_rules = BooleanField('I accept the site rules', [validators.InputRequired()])


class AppUser(UserMixin, db.Model):
    __tablename__ = 'AppUser'
    UserID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Username = db.Column(db.String(64), index=True, unique=True)
    PasswordHash = db.Column(db.String(128))
    DateJoined = db.Column(db.String(120))
    Email = db.Column(db.String(120), unique=True)
    RoleID = db.Column(db.Integer)

    def __repr__(self):
        return '<User {}>'.format(self.Username)

    def set_password(self, password):
        self.PasswordHash = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(rounds=14))

    def check_password(self, password):
        return bcrypt.checkpw(password, self.password_hash)

    def get_current_date(self):
        self.DateJoined = date.today().strftime("%m/%d/%y")


@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve

    """
    # return AppUser.query.get(user_id)
    # Just using it for  now, cuz the database is not ready yet
    return AppUser.query.get(user_id)
