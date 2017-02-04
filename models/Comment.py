from flask import g

from .Post import Post as post
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

    @classmethod
    def add(cls, form, r):
        message = {}
        valid = cls.valid(form, message)
        data = {}
        r['success'] = valid
        if valid:
            c = cls(form)
            c.save()
            data['comment'] = c.json()
            data['user'] = c.user.json()
            r['data'] = data
            notify = {
                'target_id': c.post_id,
                'target_type': TARGET_TYPE.POST,
                'action': ACTION_TYPE.COMMENT,
                'sender_id': c.user_id,
                'content': c.user.username + '评论了你的文章' + c.post.title,
            }
            notify_service.create_remind(**notify)
            subscribe = {
                'user': c.user,
                'target_id': c.id,
                'target_type': TARGET_TYPE.COMMENT,
                'reason': REASON_TYPE.COMMENT_POST
            }
            notify_service.subscribe(**subscribe)
        else:
            r['message'] = message

    @classmethod
    def valid(cls, form, message):
        p = post.query.get(form.get('post_id'))
        valid_post_exist = p is not None
        content = form.get('content', '')
        content = content.strip()
        valid_content_len = 200 >= len(content) >= 1
        if valid_post_exist  and valid_content_len:
            return True
        else:
            if not valid_post_exist:
                message['.comment-message'] = '主题不存在'
            elif not valid_content_len:
                message['.comment-message'] = '内容不能为空'
            return False

    def json(self):
        json = {
            'content': self.content,
            'created_time': self.created_time,
        }
        return json