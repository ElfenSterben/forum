from controllor import account
from . import *


@main.route('/login', methods=['post'])
@csrf.exempt
def login():
    u_json = request.get_json()
    result = account.login(u_json)
    return jsonify(result)

@main.route('/register', methods=['post'])
def register():
    u_json = request.get_json()
    account.register(u_json, r)
    return jsonify(r)
