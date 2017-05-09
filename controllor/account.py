from models.User import User
from models.SubscriptionConfig import SubscriptionConfig as SBConfig
from flask import session, g
from utils.utils import referrer_url
from forms.RegisterSchema import register_schema
from forms.LoginSchema import login_schema
from forms.SettingSchema import setting_schema
from forms.PasswordChangeSchema import pwd_change_schema

valid_str = '1234567890_qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
email_valid_str = '1234567890_qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM@.-'

def login(form):
    result = dict(success=False)
    data = login_schema.load(form)
    if data.errors == {}:
        session['user_id'] = data.data['id']
        result['success'] = True
        result['referrer'] = referrer_url('index.index')
    result['message'] = data.errors
    return result

def register(form):
    result = dict(success=False)
    data = register_schema.load(form)
    if data.errors == {}:
        result['success'] = True
        result['referrer'] = referrer_url('index.index')
        u = User.new(data.data)
        s = SBConfig()
        u.subscription_config = s
        s.save()
        session['user_id'] = u.id
    result['message'] = data.errors
    return result

def setting(form):
    result = dict(success=False)
    data = setting_schema.load(form)
    if data.errors == {}:
        result['success'] = True
        g.user.update(data.data)
    result['message'] = data.errors
    return result

def change_password(form):
    result = dict(success=False)
    data = pwd_change_schema.load(form)
    if data.errors == {}:
        _form = dict(
            password=data.data['new_password']
        )
        result['success'] = True
        g.user.update(_form)
    result['message'] = data.errors
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
