from . import *

from models.User import User


main = Blueprint('login', __name__)

@main.route('/')
def login_view():
    u = current_user()
    if u is not None:
        return redirect(url_for('index.index'))
    return render_template('login.html')


