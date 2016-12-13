from . import *

from models.Post import Post
from models.utils import log

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
    data = {}
    data['url'] = '/post/' + str(post_id)
    r['data'] = data
    n_json = request.get_json()
    Post.update(post_id, n_json, r)
    return jsonify(r)