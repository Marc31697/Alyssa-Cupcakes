from flask_sqlalchemy import SQLAlchemy
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from flask_login import UserMixin, LoginManager
from flask_marshmallow import Marshmallow
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import os

secret = os.environ.get("SECRET_KEY")

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.String(150), primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String(150), nullable = True, default = '')
    token = db.Column(db.String, default='',unique = True)
    date_created = db.Column(db.DateTime,nullable = False,default=datetime.utcnow)
    admin = db.Column(db.Boolean(), default = False)

    def __init__(self,email,first_name='',last_name='',id='',password='',token='',g_auth_verify=False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify
        self.admin = self.set_admin()

    def set_token(self,length):
        return secrets.token_hex(length)

    def get_token(self, expires_sec=300):
        serial=Serializer('secret', expires_in=expires_sec)
        return serial.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_token(token):
        serial = Serializer('secret')
        try:
            user_id=serial.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


    def set_admin(self):
        if db.session.query(User).count() == 0:
            return True
    
    def set_id(self):
        self.id = str(uuid.uuid4())
        return self.id

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash
    
    def __repr__(self):
        return f'User {self.email} has been added to the database'


class Item(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    type = db.Column(db.String(100))
    description = db.Column(db.String(200))
    price = db.Column(db.Numeric(10,2))

    def __init__(self, type, description, price, id = id):
        self.id = self.id
        self.type = type
        self.description = description
        self.price = price
    
    def __repr__(self):
        return f'Item: {self.type} ~ {self.description} ~ {self.price}'

class ItemSchema(ma.Schema):
    class Meta:
        fields = ['id','type', 'description','price']
        
item_schema = ItemSchema()
items_schema = ItemSchema(many = True)

class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    link = db.Column(db.String(500))
    height = db.Column(db.String(10))

    def __init__(self, link, height, id = id):
        self.id = self.id
        self.link = link
        self.height = height

    def __repr__(self):
        return f'Review Link: {self.link}'

class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    post = db.Column(db.String(500))
    date = db.Column(db.DateTime,nullable = False,default=datetime.utcnow)

    def __init__(self, post, id=id, date = date):
        self.id = self.id
        self.post = post
        self.date = self.date

    def __repr__(self):
        return f'Announcement: {self.post}'
    
class BugReports(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    first_name = db.Column(db.String(150), nullable = False)
    last_name = db.Column(db.String(150), nullable = False)
    email = db.Column(db.String(150), nullable = False)
    report = db.Column(db.String(500), nullable = False)
    date = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)

    def __init__(self, first_name, last_name, email, report, id=id, date = date):
        self.id = self.id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.report = report
        self.date = self.date