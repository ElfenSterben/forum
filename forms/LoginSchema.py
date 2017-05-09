from marshmallow import ValidationError, validates, validates_schema
from flask import url_for
from models.User import User
from forms.UserSchema import UserSchema

valid_str = '1234567890_qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'

class LoginSchema(UserSchema):

    @validates_schema
    def validate_username(self, data):
        username = data['username']
        password = data['password']
        u = User.query.filter_by(username=username).first()
        if u is None:
            raise ValidationError('用户名不存在', 'username')
        if u.password != password:
            raise ValidationError('用户名密码错误', 'password')
        data['id'] = u.id

login_schema = LoginSchema()