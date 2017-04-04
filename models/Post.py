from .User import User
from .Node import Node as node
from . import *
from flask import g


class Post(Model, db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    created_time = db.Column(db.Integer)
    edited_time = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    title = db.Column(db.String(30))
    content = db.Column(db.String(1000))
    hidden = db.Column(db.Boolean, default=False)
    node_id = db.Column(db.Integer, db.ForeignKey('node.id', ondelete='CASCADE'))
    comments = db.relationship('Comment', lazy='dynamic',cascade="delete, delete-orphan", backref='post')

    def __init__(self, form):
        self.created_time = timestamp()
        self.edited_time = timestamp()
        self.user = g.user
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.node_id = form.get('node_id')

    def update(self, form):
        self.edit_time = timestamp()
        self.title = form.get('title')
        self.content = form.get('content')
        self.node_id = form.get('node_id')
        self._update()

    def permission_valid(self, u):
        return u.username == self.user.username



