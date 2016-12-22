from flask import Blueprint
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import session
from flask import url_for
from flask import abort
from models.User import current_user
from functools import wraps
from hashlib import md5
from flask_uploads import (
    configure_uploads,
    UploadSet,
    patch_request_class,
    IMAGES
)


avatar = UploadSet('photos', IMAGES)

main = Blueprint('api', __name__)

def admin_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        u = current_user()
        if u is None or u.id != 1:
            abort(404)
        return f(*args, **kwargs)
    return function

def user_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        u = current_user()
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