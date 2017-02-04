import time, os
from flask import current_app
from PIL import ImageSequence

# 用 log 函数把所有输出写入到文件，这样就能很方便地掌控全局了
# 即便你关掉程序，也能再次打开来查看，这就是个时光机
def log(*args, **kwargs):
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    # 中文 windows 平台默认打开的文件编码是 gbk 所以需要指定一下
    with open('log.log', 'a', encoding='utf-8') as f:
        # 通过 file 参数可以把输出写入到文件 f 中
        # 需要注意的是 **kwargs 必须是最后一个参数
        print(dt, *args, file=f, **kwargs)

def crop_img(img, x, y, w, h):
    img_size = (160, 160)
    if hasattr(img, 'is_animated') and img.is_animated:
        frames = [f.copy() for f in ImageSequence.Iterator(img)]
        r = []
        for f in frames:
            sub_img = f.crop((x, y, x + w, y + h))
            sub_img.thumbnail(img_size)
            r.append(sub_img)
        return r
    else:
        sub_img = img.crop((x, y, x + w, y + h))
        sub_img.thumbnail(img_size)
        return sub_img

def save_avatar(img, filename, format):
    path = current_app.config['UPLOADED_PHOTOS_DEST']
    p = os.path.join(path, filename)
    save_all = False
    append_image = []
    if type(img) == list:
        save_all = True
        append_image = img[1:]
        img = img[0]

    img.save(p + '.' + format.lower(), save_all=save_all, append_images=append_image)

    return filename + '.' + format.lower()

def remove_avatar(filename):
    try:
        if filename != 'default_avatar.gif':
            path = current_app.config['UPLOADED_PHOTOS_DEST']
            p = os.path.join(path, filename)
            os.remove(p)
    except Exception as e:
        print(e)
