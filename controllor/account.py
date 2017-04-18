from models.User import User
from models.SubscriptionConfig import SubscriptionConfig as SBConfig
from flask import session

valid_str = '1234567890_qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
email_valid_str = '1234567890_qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM@.-'

def login(form):
    valid_msg = login_valid(form)
    valid = valid_msg['valid']
    result = dict(
        success=valid,
        message=valid_msg['msg']
    )
    if valid:
        session['user_id'] = valid_msg['user'].id
    return result

def register(form):
    valid_msg = register_valid(form)
    valid = valid_msg['valid']
    result = dict(
        success=valid,
        message=valid_msg['msg']
    )
    if valid:
        u = User.new(form)
        s = SBConfig()
        u.subscription_config = s
        s.save()
        session['user_id'] = u.id
    return result

def login_valid(form):
    username = form.get('username')
    password = form.get('password')
    u = User.query.filter_by(username=username).first()
    valid = u is not None and u.password == password
    result = dict(
        valid=valid,
        user=u,
        msg=dict()
    )
    msg = result['msg']
    if not valid:
        msg['.login-message'] = '用户名或密码错误'
    return result

def register_valid(form,):
    username = form.get('username')
    password = form.get('password')
    confirm_password = form.get('confirm')
    email = form.get('email')
    un_valid_msg = username_valid(username)
    pw_valid_msg = password_valid(password, confirm_password)
    e_valid_msg = email_valid(email)
    un_valid = un_valid_msg['valid']
    pw_valid = pw_valid_msg['valid']
    e_valid = e_valid_msg['valid']
    msg = dict()
    msg.update(un_valid_msg['msg'])
    msg.update(pw_valid_msg['msg'])
    msg.update(e_valid_msg['msg'])
    result = dict(
        valid=un_valid and pw_valid and e_valid,
        msg=msg
    )
    return result

def username_valid(username):
    result = dict(
        valid=False,
        msg=''
    )
    str_valid = True
    username = username.strip()
    for c in username:
        if c not in valid_str:
            str_valid = False
    length_valid = 8 <= len(username) <= 20
    u = User.query.filter_by(username=username).first()
    not_exist = u is None
    result['valid'] = str_valid and length_valid and not_exist
    msg = result['msg']
    if not str_valid:
        msg['.username-message']='输入8-20位用户名,只能使用英文字母、下划线及数字'
    elif not length_valid:
        msg['.username-message']='输入8-20位用户名,只能使用英文字母、下划线及数字'
    elif not not_exist:
        msg['.username-message']= '用户名已存在'
    return result

def password_valid(password, confirm_password):
    result = dict(
        valid=False,
        msg=dict()
    )
    password = password.strip()
    str_valid = True
    for c in password:
        if c not in valid_str:
            str_valid = False
    confirm_password = confirm_password.strip()
    length_valid = 8 <= len(password) <= 20
    confirm_valid = password == confirm_password
    result['valid'] = str_valid and length_valid and confirm_valid
    msg = result['msg']
    if not str_valid:
        msg['.password-message'] = '输入8-20位密码,只能使用英文字母、下划线及数字'
    if not length_valid:
        msg['.password-message'] = '输入8-20位密码,只能使用英文字母、下划线及数字'
    if not confirm_valid:
        msg['.confirm-message'] = '重复输入的密码'
    return result

def email_valid(email):
    result = dict(
        valid=False,
        msg=dict()
    )
    str_valid = True
    email = email.strip()
    for c in email:
        if c not in email_valid_str:
            str_valid =False

    split_email = email.split('@', 1)
    split_valid = len(split_email) == 2
    not_exist = False
    if split_valid and split_email[0] != '' and split_email[1] != '':
        host = split_email[1]
        split_host = host.split('.', 1)
        split_valid = len(split_host) == 2
        if split_valid and split_host[0] != '' and split_host[1] != '':
            u = User.query.filter_by(email=email).first()
            if u is None:
                not_exist = True
    else:
        str_valid = False
    result['valid'] = str_valid and not_exist
    msg = result['msg']
    if not str_valid:
        msg['.email-message'] = '请输入正确的邮箱'
    elif not not_exist:
        msg['.email-message'] = '邮箱已被注册'
    return result