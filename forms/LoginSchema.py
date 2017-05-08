from marshmallow import Schema, ValidationError, validates, validate
from marshmallow import fields
from flask import url_for
from models.User import User
from forms.UserSchema import UserSchema

valid_str = '1234567890_qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'

class LoginSchema(UserSchema):
    @validates('username')
    def validate_username(self, value):
        u = User.query.filter_by(username=value).first()
        if u is not None:
            raise ValidationError('用户名密码错误')
        self.user = u

    @validates('password')
    def validate_password(self, value):
        if self.user.password != value:
            raise ValidationError('用户名密码错误')

login_schema = LoginSchema()