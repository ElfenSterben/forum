from . import *
from models.Notify import Notify
from services.NotifyService import *

main = Blueprint('notify', __name__)

@main.route('/<string:notify_type>', methods=['GET'])
@user_required
def notify_view(notify_type):
    page = request.args.get('page', '1')
    if not page.isdigit():
        page = '1'
    uns = g.user.user_notifies
    paginate = uns.join(Notify).filter_by(type=notify_type).order_by(Notify.created_time.desc()).paginate(int(page), 10, False)
    un_list = paginate.items
    notify_service.read(un_list)
    data = {
        'user_notify_paginate': paginate,
        'user_notify_list': un_list,
        'selected_type': notify_type,
        'notify_types': NOTIFY_TYPE
    }
    return render_template('notify.html', **data)
