from . import *

from models.utils import log

@main.route('/user/change/info', methods=['post'])
@user_required
def update_info():
    r = {}
    s_json = request.get_json()
    u = g.user
    u.setting(s_json, r)
    return jsonify(r)

@main.route('/user/change/password', methods=['post'])
@user_required
def update_password():
    r = {}
    p_json = request.get_json()
    g.user.change_password(p_json, r)
    return jsonify(r)


@main.route('/upload/avatar', methods=['post'])
@user_required
def upload_avatar():
    u = g.user
    if 'photo' in request.files:
        folder_name = str(uuid3(NAMESPACE_DNS, str(u.id) + u.username)).replace('-','')
        try:
            filename = request.files['photo'].filename
            request.files['photo'].filename = '123.' + filename.split('.')[-1]
            filename = avatar.save(request.files['photo'],folder=folder_name, name='avatar.')
            u.avatar = avatar.url(filename)
            u.save()
        except:
            flash('请上传大小不超过2Mb的图片文件', 'error')
    return redirect(url_for('user.setting_view'))