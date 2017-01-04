from models.Post import Post
from . import *


@main.route('/post/add', methods=['post'])
@user_required
def post_add():
    r = {}
    n_json = request.get_json()
    Post.add(n_json, r)
    return jsonify(r)

@main.route('/post/update/<int:post_id>', methods=['post'])
@user_required
def post_update(post_id):
    r = {}
    p = Post.query.get(post_id)

    if p is None:
        r['success'] = False
        r['message'] = '文章不存在'
    elif not p.permission_valid(g.user):
        r['success'] = False
        r['message'] = '不是你的文章'
    else:
        data = {}
        data['url'] = '/post/' + str(post_id)
        r['data'] = data
        n_json = request.get_json()
        p.update(n_json, r)

    return jsonify(r)

# @main.route('/post/<int:post_id>/vote', methods=['get'])
# @user_required
# def post_vote(post_id):
#     r = {}
#     p = Post.query.get(post_id)
#     if p is None:
#         r['success'] = False
#         r['message']['.vote-message'] = '文章不存在'
#     else:
#         p.vote += 1
#         p.save()
#         r['success'] = True
#     return jsonify(r)