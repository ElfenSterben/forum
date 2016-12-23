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
        folder_name = str(uuid3(NAMESPACE_DNS, str(u.id) + u.username)).replace('-','')
        print(request.files['photo'])
        print(avatar.get_basename(request.files['photo'].filename))
        filename = avatar.save(request.files['photo'],folder=folder_name, name='avatar.')
        print(avatar.url(filename))
        u.avatar = avatar.url(filename)
        u.save()

            # flash('请上传图片文件', 'error')
    return redirect(url_for('user.setting_view'))