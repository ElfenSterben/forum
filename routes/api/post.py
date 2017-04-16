from controllor import post
from . import *


@main.route('/post/add', methods=['post'])
@user_required
def post_add():
    form = request.get_json()
    result = post.add(form)
    return jsonify(result)

@main.route('/post/update/<int:post_id>', methods=['post'])
@user_required
def post_update(post_id):
    form = request.get_json()
    result = post.update(post_id, form)
    return jsonify(result)

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