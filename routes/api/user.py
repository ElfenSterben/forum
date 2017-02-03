from . import *
from uuid import uuid3, NAMESPACE_DNS
from PIL import Image
from io import BytesIO, StringIO
import os

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
        form = request.form
        folder_name = str(uuid3(NAMESPACE_DNS, str(u.id) + u.username)).replace('-','')
        try:
            size_big = (76, 76)
            x = int(form['x'])
            y = int(form['y'])
            w = int(form['nw'])
            h = int(form['nh'])
            filename = request.files['photo'].filename
            img = Image.open(request.files['photo'])
            sub_img = img.crop((x, y, x+w, y+h))
            sub_img.thumbnail(size_big)
            request.files['photo'].filename = '123.' + filename.split('.')[-1]
            filename = avatar.save(sub_img, folder=folder_name, name='avatar.jpg')
            u.avatar = avatar.url(filename)
            u.save()
        except Exception as e:
            print(e)
            flash('请上传大小不超过2Mb的图片文件', 'error')
    return redirect(url_for('user.setting_view'))



def save_avatar(folder, img):
    img_size = {
        'big': (76, 76),
        'middle': (48, 48),
        'small': (30, 30),
    }

    path = './static'
    path = os.path.join(path, folder)
    if not os.path.exists(path):
        os.mkdir(path)
    for k, v in img_size.items():
        img.thumbnail(v)
        img.save(path + 'avatar_' + k + '.jpg')

