from app import db_user
from flask.ext.login import UserMixin

ROLE_USER = 0
ROLE_ADMIN = 1   

class User(UserMixin, db_user.Model):
    id = db_user.Column(db_user.Integer, primary_key = True)
    name = db_user.Column(db_user.String(64), index = True, unique = True)
    password = db_user.Column(db_user.String(64), index = True, unique = False)
    rights = db_user.Column(db_user.Integer, index = True, unique = False)
    date = db_user.Column(db_user.DateTime, index = True)

    def __repr__(self):
        return '<User %r>' % (self.name)
