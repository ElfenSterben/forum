from . import *

from models.User import User

main = Blueprint('user', __name__)

@main.route('/<string:username>/info')
def info_view(username):
    data = User.view(username)
    return render_template('user_info.html', **data)

@main.route('/setting')
def setting_view():
    return render_template('user_setting.html')

