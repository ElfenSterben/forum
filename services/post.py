from flask import url_for
from flask import g
from models.Post import Post
from models.Node import Node
from services.NotifyService import notify_service, TARGET_TYPE, REASON_TYPE

def add(form):
    result = {}
    message = {}
    valid = form_valid(form, message)
    data = {}
    result['success'] = valid
    if valid:
        p = Post.new(form)
        subscribe_post(p)
        data['url'] = url_for('post.view',post_id=p.id)
        result['data'] = data
    else:
        result['message'] = message

def update(post_id, form):
    result = {}
    message = {}
    p = g.user.posts.query.filter_by(id=post_id)
    if p is None:
        result['success'] = False
        result['message'] = '文章不存在'
        return result
    valid = form_valid(form, message)
    result['success'] = valid
    if valid:
        p.update(form)
    result['message'] = message
    return result

def subscribe_post(post):
    subscribe = {
        'user': post.user,
        'target_id': post.id,
        'target_type': TARGET_TYPE.POST,
        'reason': REASON_TYPE.CREATE_POST
    }
    notify_service.subscribe(**subscribe)

def form_valid(form, message):
    nid = form.get('node_id')
    n = Node.query.filter_by(id=nid)
    valid_node_exist = n is not None
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