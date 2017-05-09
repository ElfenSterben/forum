from . import *
from uuid import uuid3, NAMESPACE_DNS
from PIL import Image
from utils.utils import save_avatar, remove_avatar, crop_img
from flask import current_app
import time
from controllor.account import setting, change_password

@main.route('/user/change/info', methods=['post'])
@user_required
def update_info():
    s_json = request.get_json()
    result = setting(s_json)
    return jsonify(result)

@main.route('/user/change/password', methods=['post'])
@user_required
def update_password():
    p_json = request.get_json()
    result = change_password(p_json)
    return jsonify(result)

@main.route('/upload/avatar', methods=['post'])
@user_required
def upload_avatar():
    u = g.user
    if 'photo' in request.files:
        form = request.form
        filename = str(uuid3(NAMESPACE_DNS, str(u.id) + u.username + str(time.time()))).replace('-','')
        try:
            x = int(form['x'])
            y = int(form['y'])
            w = int(form['nw'])
            h = int(form['nh'])
            img = Image.open(request.files['photo'])
            format = img.format
            croped_img = crop_img(img, x, y, w, h)
            filename = save_avatar(croped_img, filename, format)
            url_path = current_app.config['UPLOADED_PHOTOS_URL']
            old_name = u.avatar.split(url_path)[1]
            remove_avatar(old_name)
            u.avatar = url_path + filename
            u.save()
        except Exception as e:
            print(e)
            flash('请上传大小不超过2Mb的图片文件', 'error')
    return redirect(url_for('user.setting_view'))



