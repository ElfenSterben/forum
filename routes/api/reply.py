from . import *

from models.Reply import Reply
from models.utils import log

@main.route('/reply/add', methods=['post'])
@user_required
def comment_add():
    r = {}
    c_json = request.get_json()
    Reply.add(c_json, r)
    return jsonify(r)