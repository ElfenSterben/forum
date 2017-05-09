from flask import url_for, g, abort, request, current_app
from models.Post import Post
from models.Node import Node
from forms.PostSchema import post_schema
from forms.NodeSchema import node_schema, node_schemas
from forms.UserSchema import user_schema
from services.NotifyService import notify_service, TARGET_TYPE, REASON_TYPE


def add(form):
    result = dict(success=False)
    res = post_schema.load(form)
    if res.errors == {}:
        result['success'] = True
        p = Post.new(res.data)
        subscribe_post(p)
        data = dict(url=p.url())
        result['data'] = data
    result['message'] = res.errors
    return result

def page(p, node_name=None):
    if not p.isdigit():
        p = '1'
    page = int(p)
    pre_page = current_app.config.get('POST_PRE_PAGE', 20)
    node = Node.query.filter_by(name=node_name).first()
    nl = Node.query.order_by(Node.edited_time).all()
    node_list = node_schema.dump(nl, many=True).data
    result = dict(
        success=True,
        node_list=node_list,
        selected_node=node_name,
    )
    if node_name != 'all' and node is None:
        result['success'] = False
        result['message'] = {
            'node': ['节点不存在'],
        }
        return result
    if node_name == 'all':
        query = Post.query
    else:
        query = node.posts
    paginate = query.order_by(Post.edited_time.desc()).paginate(page, pre_page, False)
    post_list = paginate.items
    pl = []
    for p in post_list:
        _data = dict(
            post=post_schema.dump(p),
            user=user_schema.dump(p.user),
            node=node_schema.dump(p.node)
        )
        pl.append(_data)
    data = dict(
        current_page=paginate.page,
        pages=paginate.pages,
        post_list=pl,
    )
    result['data'] = data
    return result

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
    if not valid:
        abort(403)
    node_list = Node.query.filter_by(hidden=False)
    data = dict(
        node_list=node_list,
        post=p,
    )
    return data

def update(post_id, form):
    result = dict(success=False)
    res = post_schema.load(form)
    p = g.user.posts.filter_by(id=post_id).first()
    if p is None:
        abort(404)
    if res.errors == {}:
        result['success'] = True
        p.update(res.data)
        data = dict(url=p.url())
        result['data'] = data
    result['message'] = res.errors
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
