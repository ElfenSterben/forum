from . import *
from models.Notify import Notify
from services.NotifyService import *

main = Blueprint('notify', __name__)

@main.route('/<string:notify_type>', methods=['GET'])
@user_required
def notify_view(notify_type):
    page = request.args.get('page', '1')
    data = g.user.notifies(notify_type, page)
    return render_template('notify.html', **data)
