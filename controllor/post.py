from flask import url_for, g, abort, request, current_app
from models.Post import Post
from models.Node import Node
from services.NotifyService import notify_service, TARGET_TYPE, REASON_TYPE


def add(form):
    result = dict(
        success=False,
        message=dict(),
        data=dict()
    )
    valid_msg = form_valid(form)
    valid = valid_msg['valid']
    result['success'] = valid
    result['message'] = valid_msg['message']
    if valid:
        p = Post.new(form)
        subscribe_post(p)
        data = dict(
            url=url_for('post.view', post_id=p.id)
        )
        result['data'] = data
    return result

def page(p, node_name=None):
    if not p.isdigit():
        p = '1'
    page = int(p)
    pre_page = current_app.config.get('POST_PRE_PAGE', 20)
    if node_name is None:
        query = Post.query
    else:
        node = Node.query.filter_by(name=node_name).first()
        if node is None:
            abort(404)
        query = node.posts
    paginate = query.order_by(Post.created_time.desc()).paginate(page, pre_page, False)
    post_list = paginate.items
    node_list = Node.query.all()
    data = {
        'post_list': post_list,
        'paginate': paginate,
        'node_list': node_list,
        'selected_node': node_name,
    }
    return data

def view(post_id, comment_page):
    p = Post.query.get(post_id)
    if p is None:
        abort(404)
    if not comment_page.isdigit():
        comment_page = '1'
    page = int(comment_page)
    comment_pre_page = current_app.config.get('COMMENT_PRE_PAGE', 15)
    comment_paginate = p.comments.paginate(page, comment_pre_page, False)
    post_comments = comment_paginate.items
    data = {
        'post': p,
        'comment_paginate': comment_paginate,
        'post_comments': post_comments,
    }
    return data

def edit(post_id):
    p = Post.query.get(post_id)
    if p is None:
        abort(404)
    valid = p.permission_valid(g.user)
    node_list = Node.query.filter_by(hidden=False)
    if not valid:
        abort(403)
    data = dict(
        node_list=node_list,
        post=p,
    )
    return data

def update(post_id, form):
    p = g.user.posts.query.filter_by(id=post_id)
    if p is None:
        abort(404)
    valid_msg = form_valid(form)
    valid = valid_msg['valid']
    result = dict(
        success=valid,
        message=valid_msg['msg']
    )
    if valid:
        p.update(form)
    return result

def delete(post_id):
    p = Post.query.get(post_id)
    if p is None:
        abort(404)
    valid = p.permission_valid(g.user)
    if valid:
        p.comments.delete()
        p.delete()
    abort(403)

def subscribe_post(post):
    subscribe = {
        'user': post.user,
        'target_id': post.id,
        'target_type': TARGET_TYPE.POST,
        'reason': REASON_TYPE.CREATE_POST
    }
    notify_service.subscribe(**subscribe)

def form_valid(form):
    result = dict(
        valid=False,
        msg=dict()
    )
    nid = form.get('node_id')
    n = Node.query.filter_by(id=nid)
    valid_node_exist = n is not None
    valid_title_len = 30 >= len(form.get('title', '')) >= 2
    valid_content_len = 1000 >= len(form.get('content', '')) >= 10
    result['valid'] = valid_node_exist and valid_title_len and valid_content_len
    msg = result['msg']
    if not valid_title_len:
        msg['.post-title-message'] = '标题请输入2-30个字符'
    if not valid_content_len:
        msg['.post-content-message'] = '内容请输入10-1000个字符'
    if not valid_node_exist:
        msg['.post-node-message'] = '节点不存在'
    return result
