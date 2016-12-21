from flask import Blueprint
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import session
from flask import url_for
from flask import abort
from flask import flash


from models.User import current_user, timestamp
from .api import admin_required
from .api import user_required

hostname = 'kaede'

data_list = {
    'hostname': hostname,
    'current_time': timestamp(),
}