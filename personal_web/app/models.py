from app import db
from flask.ext.login import UserMixin
'''
ROLE_USER = 0
ROLE_ADMIN = 1   

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    password = db.Column(db.String(64), index = True, unique = False)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    license = db.relationship('License', backref = 'author', lazy = 'dynamic')

    def __repr__(self):
        return '<User %r>' % (self.username)
    
class License(db.Model):
    
    id = db.Column(db.Integer, primary_key = True)
    featurecode = db.Column(db.Text, index = True, unique = False)
    machinetype = db.Column(db.String(64), index = True, unique = False)
    remark = db.Column(db.Text, index = True, unique = False)
    licenseuse = db.Column(db.Text, index = True, unique = True)
    datetime = db.Column(db.DateTime, index = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return '<License %r>' % (self.featurecode)    
 
class Machine(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text, index = True, unique = True)
    value = db.Column(db.Integer, index = True, unique = True)

    def __repr__(self):
        return '<Machine: %r>' % (self.name)
'''
