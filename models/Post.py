from .User import User, current_user
from .Node import Node as node
from . import *


class Post(Model, db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    created_time = db.Column(db.Integer)
    edited_time = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(30))
    content = db.Column(db.String(1000))
    hidden = db.Column(db.Boolean, default=False)
    node_id = db.Column(db.Integer, db.ForeignKey('node.id'))
    comments = db.relationship('Comment', backref='post')

    def __init__(self, form):
        self.created_time = timestamp()
        self.edited_time = timestamp()
        self.user = current_user()
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.node_id = form.get('node_id')

    @classmethod
    def update(cls, id, form, r):
        p = cls.query.get(id)
        message = {}
        pm_valid = cls.permission_valid(p, message)
        form_valid = cls.content_valid(form, message)
        valid = pm_valid and form_valid
        r['success'] = valid
        if valid:
            p.edit_time = timestamp()
            p.title = form.get('title', '')
            p.content = form.get('content', '')
            p.save()
        r['message'] = message

    @classmethod
    def add(cls, form, r):
        message = {}
        valid = cls.content_valid(form, message)
        data = {}
        r['success'] = valid
        if valid:
            p = cls(form)
            p.save()
            data['url'] = url_for('post.view',post_id=p.id)
            r['data'] = data
        else:
            r['message'] = message

    @classmethod
    def content_valid(cls, form, message):
        n = node.query.get(form.get('node_id'))
        valid_node_exist = n is not None
        valid_title_len = 30 > len(form.get('title', '')) > 2
        valid_content_len = 1000 > len(form.get('content', '')) > 10
        if valid_node_exist and valid_title_len and valid_content_len:
            return True
        else:
            if not valid_title_len:
                message['.post-title-message'] = '标题请输入2-20个字符'
            if not valid_content_len:
                message['.post-content-message'] = '内容请输入10-1000个字符'
            if not valid_node_exist:
                message['.post-node-message'] = '节点不存在'
            return False

    @classmethod
    def post_delete(cls, post_id):
        p = cls.query.get(post_id)
        message = {}
        valid = cls.permission_valid(p, message)
        if valid:
            super(cls, p).delete()



    @classmethod
    def permission_valid(cls, post, message):
        u = current_user()
        result = False
        if post is not None:
            result = u.username == post.user.username
        if not result:
            message['post-exist-message'] = '文章不存在'

        return result


