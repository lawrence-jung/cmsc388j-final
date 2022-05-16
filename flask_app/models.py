from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager
from . import config
from .utils import current_time
import base64

@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()

class id_counter(db.Document):
    value = db.IntField()

class User(db.Document, UserMixin):
    username = db.StringField(required=True, unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)
    groups = db.ListField()

    # Returns unique string identifying our object
    def get_id(self):
        return self.username
    
    def get_groups(self):
        return self.groups


class Comment(db.Document):
    commenter = db.StringField(required=True)
    content = db.StringField(required=True, min_length=1, max_length=500)
    date = db.StringField(required=True)

class Group(db.Document):
    g_id = db.IntField()
    members = db.ListField()
    name = db.StringField(required=True)
    expiry = db.IntField(required=True)
    open_invite = db.BooleanField(default=False)
    today = db.StringField()
    over = db.BooleanField(default=False)

    subs = db.ListField()
    comments = db.ListField()

    def get_members(self):
        mems = []
        for m in self.members:
            mems.append(m.username)
        return mems

class Submission(db.Document):
    song = db.StringField()
