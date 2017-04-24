from models.Comment import Comment
from models.Reply import Reply
from controllor import reply
from . import *


@main.route('/reply/add', methods=['post'])
@user_required
def reply_add():
    r_json = request.get_json()
    result = reply.add(r_json)
    return jsonify(result)

@main.route('/comment/<int:comment_id>/replies', methods=['get'])
def reply_view(comment_id):
    page = request.args.get('page', '1')
    result = reply.page(comment_id, page)
    return jsonify(result)