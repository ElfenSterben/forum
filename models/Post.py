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

    def update(self, form, r):
        message = {}
        form_valid = self.form_valid(form, message)
        r['success'] = form_valid
        if form_valid:
            self.edit_time = timestamp()
            self.title = form.get('title', '')
            self.content = form.get('content', '')
            self.node_id = form.get('node_id', '1')
            self.save()
        r['message'] = message

    @classmethod
    def add(cls, form, r):
        message = {}
        valid = cls.form_valid(form, message)
        data = {}
        r['success'] = valid
        if valid:
            p = cls(form)
            p.save()
            subscribe = {
                'user': p.user,
                'target_id': p.id,
                'target_type': TARGET_TYPE.POST,
                'reason': REASON_TYPE.CREATE_POST
            }
            notify_service.subscribe(**subscribe)
            data['url'] = url_for('post.view',post_id=p.id)
            r['data'] = data
        else:
            r['message'] = message

    @classmethod
    def form_valid(cls, form, message):
        nid = form.get('node_id')
        if nid is not None:
            n = node.query.get(nid)
        valid_node_exist = nid is not None and n
        valid_title_len = 30 >= len(form.get('title', '')) >= 2
        valid_content_len = 1000 >= len(form.get('content', '')) >= 10
        if valid_node_exist and valid_title_len and valid_content_len:
            return True
        else:
            if not valid_title_len:
                message['.post-title-message'] = '标题请输入2-30个字符'
            if not valid_content_len:
                message['.post-content-message'] = '内容请输入10-1000个字符'
            if not valid_node_exist:
                message['.post-node-message'] = '节点不存在'
            return False

    def permission_valid(self, u):
        return u.username == self.user.username



