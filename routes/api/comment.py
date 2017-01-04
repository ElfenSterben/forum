from models.Comment import Comment
from . import *


@main.route('/comment/add', methods=['post'])
@user_required
def comment_add():
    r = {}
    c_json = request.get_json()
    Comment.add(c_json, r)
    return jsonify(r)