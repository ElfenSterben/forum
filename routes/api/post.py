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