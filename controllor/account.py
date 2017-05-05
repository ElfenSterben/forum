from models.User import User
from models.SubscriptionConfig import SubscriptionConfig as SBConfig
from flask import session
from utils.utils import referrer_url
from forms.RegisterSchema import register_schema

valid_str = '1234567890_qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
email_valid_str = '1234567890_qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM@.-'

def login(form):
    valid_msg = login_valid(form)
    valid = valid_msg['valid']
    result = dict(
        success=valid,
        message=valid_msg['msg'],
        referrer=referrer_url('index.index')
    )
    if valid:
        session['user_id'] = valid_msg['user'].id
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
