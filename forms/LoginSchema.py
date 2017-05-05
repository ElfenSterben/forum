from marshmallow import Schema, ValidationError, validates, validate
from marshmallow import fields
from flask import url_for
from models.User import User
from forms.UserSchema import UserSchema

valid_str = '1234567890_qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'

class LoginSchema(UserSchema):
    username=fields.Str(required=True, load_only=True)
    password = fields.Email(required=True, error='请输入正确的邮箱', load_only=True)

    @validates('username')
    def validate_username(self, value):
        u = User.query.filter_by(username=value).first()
        if u is None:
            raise ValidationError('用户名已存在')

login_schema = LoginSchema()