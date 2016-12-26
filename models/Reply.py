from . import *
from flask import g
from .User import User
from .Comment import Comment

class Reply(Model, db.Model):
    __tablename__ = 'reply'
    id = db.Column(db.Integer, primary_key=True)
    created_time = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('reply_user.id'))
    comment_id = db.Column(db.Integer, db.Foreignkey('comment.id'))
    replied_id = db.Column(db.Integer, db.ForeignKey('replied_user.id'))
    content = db.Column(db.String(1000))
    hidden = db.Column(db.Boolean, default=False)

    def __init__(self, form):
        self.created_time = timestamp()
        self.reply_user = g.user
        self.replied_user = User.query.filter_by(username=form.get('username')).first()
        self.comment = form.get('comment_id')
        self.content = form.get('content', '')

    @classmethod
    def add(cls, form, r):
        message = {}
        valid = cls.valid(form, message)
        data = {}
        r['success'] = valid
        if valid:
            r = cls(form)
            r.save()
            data['reply'] = r.json()
            data['reply_user'] = r.reply_user.json()
            data['replied_user'] = r.replied_user.json() if r.replied_user is not None else None
            r['data'] = data
        else:
            r['message'] = message

    @classmethod
    def valid(cls, form, message):
        c = Comment.query.get(form.get('comment_id'))
        valid_comment_id_exist = c is not None
        content = form.get('content', '')
        content = content.strip()
        valid_content_len = 1000 >= len(content) >= 1
        if valid_comment_id_exist  and valid_content_len:
            return True
        else:
            if not valid_comment_id_exist:
                message['.reply-message'] = '评论不存在请刷新后再试'
            elif not valid_content_len:
                message['.reply-message'] = '内容长度不符'
            return False

    def json(self):
        json = {
            'content': self.content,
            'created_time': self.created_time,
        }
        return json