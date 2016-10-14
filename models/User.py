from . import timestamp
from . import Model, db
from flask import session


def current_user():
    u_id = session.get('user_id')
    if u_id is not None:
        return User.query.get(u_id)
    return None


class User(Model, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    created_time = db.Column(db.Integer)
    nickname = db.Column(db.String(20), unique=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True)
    avatar = db.Column(db.String(50), default='/static/avatar/default_avatar.gif')
    posts = db.relationship('Post', backref='user')
    comments = db.relationship('Comment', backref='user')

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
        if u is None or u.password != password:
            message['.login-message'] = '用户名或密码错误'
            return False
        else:
            session['user_id'] = u.id
            return True

    @classmethod
    def register(cls, form, r):
        message = {}
        valid = cls.register_valid(form, message)
        r['success'] = valid
        if valid:
            u = cls(form)
            u.save()
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
        if success:
            return True
        else:
            return False

    @classmethod
    def username_valid(cls, username, message):
        length_valid = 8 <= len(username) <= 20
        u = User.query.filter_by(username=username).first()
        not_exist = u is None
        if length_valid and not_exist:
            return True
        if not length_valid:
            message['.username-message'] = '请输入8-20位用户名'
        elif not not_exist:
            message['.username-message'] = '用户名已存在'
        return False

    @classmethod
    def password_valid(cls, password, confirm_password, message):
        length_valid = 8 <= len(password) <= 20
        confirm_valid = password == confirm_password
        if length_valid and confirm_valid:
            return True
        if not length_valid:
            message['.password-message'] = '请输入8-20位密码'
        if not confirm_valid:
            message['.confirm-message'] = '请输入相同的密码'
        return False

    @classmethod
    def email_valid(cls, email, message):
        split_email = email.split('@')
        split_valid = len(split_email) == 2
        if not split_valid:
            message['.email-message'] = '请输入正确的邮箱'
            return False

        before_valid = split_email[0] != ''
        after_valid = split_email[1] != ''

        if before_valid and after_valid:
            return True
        else:
            message['.email-message'] = '请输入正确的邮箱'
            return False

    def json(self):
        json = {
            'username':self.username,
            'avatar': self.avatar
        }
        return json