from functools import wraps

from .. import *

main = Blueprint('api', __name__)

def admin_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        u = g.user
        if u is None or u.id != 1:
            abort(404)
        return f(*args, **kwargs)
    return function

def user_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        u = g.user
        if u is None:
            return redirect(url_for('login.login_view'))
        else:
            return f(*args, **kwargs)
    return function

from . import login
from . import node
from . import post
from . import comment
from . import user
from . import reply