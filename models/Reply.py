from . import *
from flask import g
from .User import User
from .Comment import Comment


class Reply(Model, db.Model):
    __tablename__ = 'reply'
    id = db.Column(db.Integer, primary_key=True)
    created_time = db.Column(db.Integer)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id', ondelete='CASCADE'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    content = db.Column(db.String(1000))
    hidden = db.Column(db.Boolean, default=False)

    def __init__(self, form):
        self.created_time = timestamp()
        self.sender = g.user
        self.receiver = User.query.filter_by(username=form.get('receiver_name')).first()
        self.comment_id = form.get('comment_id')
        self.content = form.get('content', '')

    @classmethod
    def add(cls, form, r):
        message = {}
        valid = cls.valid(form, message)
        data = {}
        r['success'] = valid
        if valid:
            reply = cls(form)
            reply.save()
            data['reply'] = reply.json()
            data['sender'] = reply.sender.json()
            data['receiver'] = reply.receiver.json() if reply.receiver is not None else None
            r['data'] = data
            if reply.receiver is not None:
                print(form)
                notify = {
                    'target_id': form.get('reply_id'),
                    'target_type': TARGET_TYPE.REPLY,
                    'action': ACTION_TYPE.REPLY,
                    'sender_id': reply.sender_id,
                    'content': reply.sender.username + '在' + reply.comment.post.title + '回复了你',
                }
                subscribe = {
                    'user': reply.sender,
                    'target_id': reply.id,
                    'target_type': TARGET_TYPE.REPLY,
                    'reason': REASON_TYPE.REPLY_REPLY
                }
            else:
                notify = {
                    'target_id': reply.comment_id,
                    'target_type': TARGET_TYPE.COMMENT,
                    'action': ACTION_TYPE.REPLY,
                    'sender_id': reply.sender_id,
                    'content': reply.sender.username + '在' + reply.comment.post.title + '回复了你',
                }
                subscribe = {
                    'user': reply.sender,
                    'target_id': reply.id,
                    'target_type': TARGET_TYPE.REPLY,
                    'reason': REASON_TYPE.REPLY_COMMENT
                }
            notify_service.create_remind(**notify)
            notify_service.subscribe(**subscribe)
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
            'id': self.id,
            'content': self.content,
            'created_time': self.created_time,
        }
        return json