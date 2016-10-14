from . import *

main = Blueprint('logout', __name__)

@main.route('/')
def logout():
    session.pop('user_id')
    return redirect(url_for('index.index'))


