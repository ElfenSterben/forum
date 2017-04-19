from flask import g

from . import *

class Comment(Model, db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    created_time = db.Column(db.Integer)
    edited_time = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    content = db.Column(db.String(200))
    hidden = db.Column(db.Boolean, default=False)
    replies = db.relationship('Reply', lazy='dynamic',cascade="delete, delete-orphan", backref='comment')
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'))

    def __init__(self, form):
        self.created_time = timestamp()
        self.edited_time = timestamp()
        self.user = g.user
        self.content = form.get('content', '')
        self.post_id = form.get('post_id')

    def json(self):
        json = {
            'content': self.content,
            'created_time': self.created_time,
        }
        return json


