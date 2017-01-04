from models.User import User
from . import *


@main.route('/login', methods=['post'])
@csrf.exempt
def login():
    r = {}
    u_json = request.get_json()
    User.login(u_json, r)
    return jsonify(r)

@main.route('/register', methods=['post'])
def register():
    r = {}
    u_json = request.get_json()
    User.register(u_json, r)
    return jsonify(r)
