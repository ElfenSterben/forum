from . import *

from models.User import User


main = Blueprint('user', __name__)

@main.route('/<string:username>/info')
def info_view(username):
    user = User.query.filter_by(username=username).first()
    u = current_user()

    data = {
        'check_user': user,
        'user': u
    }
    return render_template('user_info.html', **data)


@main.route('/setting')
def setting_view():
    u = current_user()
    data = {
        'user': u
    }
    return render_template('user_setting.html', **data)

