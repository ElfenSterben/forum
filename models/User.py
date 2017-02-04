from flask import session
from .SubscriptionConfig import SubscriptionConfig as SBConfig
from . import *
from .Notify import Notify

valid_str = '1234567890_qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
email_valid_str = '1234567890_qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM@.-'

class User(Model, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    created_time = db.Column(db.Integer)
    nickname = db.Column(db.String(20), unique=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True)
    avatar = db.Column(db.String(200), default='/static/avatar/default_avatar.gif')
    subscription_config = db.relationship('SubscriptionConfig',cascade="delete, delete-orphan", uselist=False, backref='user')

    posts = db.relationship('Post', lazy='dynamic',cascade="delete, delete-orphan", backref='user')
    comments = db.relationship('Comment', lazy='dynamic',cascade="delete, delete-orphan", backref='user')
    sends = db.relationship('Reply', lazy='dynamic', backref='sender',cascade="delete, delete-orphan", foreign_keys='Reply.sender_id')
    receives = db.relationship('Reply', lazy='dynamic', backref='receiver',cascade="delete, delete-orphan", foreign_keys='Reply.receiver_id')
    subscriptions = db.relationship('Subscription', lazy='dynamic',cascade="delete, delete-orphan", backref='user')
    user_notifies = db.relationship('UserNotify', lazy='dynamic',cascade="delete, delete-orphan", backref='user')

    def __init__(self, form):
        super(User, self).__init__()
        self.username = form.get('username')
        self.nickname = self.username
        self.password = form.get('password')
        self.email = form.get('email')

        self.created_time = timestamp()

    @classmethod
    def login(cls, form, r):
        message = {}
        r['success'] = cls.login_valid(form, message)
        r['message'] = message

    @classmethod
    def login_valid(cls, form, message):
        username = form.get('username')
        password = form.get('password')
        u = cls.query.filter_by(username=username).first()
        valid = u is None or u.password != password
        if valid:
            message['.login-message'] = '用户名或密码错误'
        else:
            session['user_id'] = u.id
        return not valid

    @classmethod
    def register(cls, form, r):
        message = {}
        valid = cls.register_valid(form, message)
        r['success'] = valid
        if valid:
            u = cls(form)
            s = SBConfig()
            u.save()
            u.subscription_config = s
            s.save()
            u = cls.query.filter_by(username=u.username).first()
            session['user_id'] = u.id
        else:
            r['message'] = message

    @classmethod
    def register_valid(cls, form, message):
        username = form.get('username')
        password = form.get('password')
        confirm_password = form.get('confirm')
        email = form.get('email')
        username_valid = cls.username_valid(username, message)
        password_valid = cls.password_valid(password, confirm_password, message)
        email_valid = cls.email_valid(email, message)
        success = username_valid and email_valid and password_valid
        return success

    @classmethod
    def username_valid(cls, username, message):
        username = username.strip()
        for c in username:
            if c not in valid_str:
                message['.username-message'] = '输入8-20位用户名,只能使用英文字母、下划线及数字'
                return False

        length_valid = 8 <= len(username) <= 20
        u = User.query.filter_by(username=username).first()
        not_exist = u is None

        if not length_valid:
            message['.username-message'] = '输入8-20位用户名,只能使用英文字母、下划线及数字'
        elif not not_exist:
            message['.username-message'] = '用户名已存在'

        return length_valid and not_exist

    @classmethod
    def password_valid(cls, password, confirm_password, message):
        password = password.strip()
        for c in password:
            if c not in valid_str:
                message['.password-message'] = '输入8-20位密码,只能使用英文字母、下划线及数字'
                return False

        confirm_password = confirm_password.strip()
        length_valid = 8 <= len(password) <= 20
        confirm_valid = password == confirm_password

        if not length_valid:
            message['.password-message'] = '输入8-20位密码,只能使用英文字母、下划线及数字'
        if not confirm_valid:
            message['.confirm-message'] = '重复输入的密码'

        return length_valid and confirm_valid

    @classmethod
    def email_valid(cls, email, message):
        email = email.strip()
        for c in email:
            if c not in email_valid_str:
                message['.email-message'] = '请输入正确的邮箱'
                return False

        split_email = email.split('@', 1)
        split_valid = len(split_email) == 2
        if split_valid and split_email[0] != '' and split_email[1] != '':
            host = split_email[1]
            split_host = host.split('.', 1)
            split_valid = len(split_host) == 2
            if split_valid and split_host[0] != '' and split_host[1] != '':
                u = cls.query.filter_by(email=email).first()
                if u is None:
                    return True
                message['.email-message'] = '邮箱已被注册'
        else:
            message['.email-message'] = '请输入正确的邮箱'
        return False

    def setting_valid(self, form, message):
        email = form.get('email')
        email_valid = User.email_valid(email, message)
        return email_valid

    def change_password_valid(self, form, message):
        old = form.get('old-password')
        new = form.get('new-password')
        confirm = form.get('confirm-password')
        old_valid = old == self.password
        new_valid = User.password_valid(new, confirm, message)

        if not old_valid:
            message['.old-psw-message'] = '请输入当前密码'

        return new_valid and old_valid

    def setting(self, form, r):
        message = {}
        valid = self.setting_valid(form, message)
        r['success'] = valid
        if valid:
            self.email = form.get('email')
            self.save()
        else:
            r['message'] = message

    def change_password(self, form, r):
        message = {}
        valid = self.change_password_valid(form, message)
        r['success'] = valid
        if valid:
            self.password = form.get('new-password')
        else:
            r['message'] = message

    def last_user_notify(self, type):
        return self.user_notifies.join(Notify).filter_by(
            type=type
        ).order_by(
            Notify.created_time.desc()
        ).first()

    def get_subscriptions(self):
        ss = self.subscriptions
        subscriptions = []
        for s in ss:
            if getattr(self.subscription_config, s.action) is True:
                subscriptions.append(s)
        return subscriptions

    def json(self):
        json = {
            'username':self.username,
            'avatar': self.avatar
        }
        return json