from . import *

from models.utils import log



@main.route('/user/change/info', methods=['post'])
@user_required
def update_info():
    r = {}
    s_json = request.get_json()
    u = current_user()
    u.setting(s_json, r)
    return jsonify(r)

@main.route('/user/change/password', methods=['post'])
@user_required
def update_password():
    r = {}
    p_json = request.get_json()
    u = current_user()
    u.change_password(p_json, r)
    return jsonify(r)


@main.route('/upload/avatar', methods=['post'])
@user_required
def upload_avatar():
    u = current_user()
    if 'photo' in request.files:
        filename = avatar.save(request.files['photo'])
        u.avatar = '/static/avatar/' + filename
        u.save()
    return redirect(url_for('user.setting_view'))