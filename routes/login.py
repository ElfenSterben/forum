from . import *

main = Blueprint('login', __name__)

@main.route('/')
def login_view():
    u = g.user
    if u is not None:
        return redirect(url_for('index.index'))
    return render_template('login.html')


