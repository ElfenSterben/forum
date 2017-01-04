from models.Comment import Comment
from models.Reply import Reply
from . import *


@main.route('/reply/add', methods=['post'])
@user_required
def reply_add():
    r = {}
    r_json = request.get_json()
    Reply.add(r_json, r)
    return jsonify(r)

@main.route('/comment/<int:comment_id>/replies', methods=['get'])
def reply_view(comment_id):
    c = Comment.query.get(comment_id)
    if c is None:
        abort(404)
    r = {}
    page = request.args.get('page', '1')
    if not page.isdigit():
        page = '1'
    page = int(page)
    reply_pre_page = current_app.config.get('REPLY_PRE_PAGE', 15)
    reply_paginate = c.replies.paginate(page, reply_pre_page, False)
    comment_replies = reply_paginate.items

    data = {
        'comment': c,
        'reply_paginate': reply_paginate,
        'comment_replies': comment_replies,
    }
    r['success'] = True
    r['data'] = render_template('reply_list.html', **data)
    return jsonify(r)