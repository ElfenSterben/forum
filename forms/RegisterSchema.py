from marshmallow import Schema, ValidationError, validates, validate
from marshmallow import fields
from flask import url_for
from models.User import User
from forms.UserSchema import UserSchema

valid_str = '1234567890_qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'

class RegisterSchema(UserSchema):
    confirm=fields.Str(required=True, load_only=True)
    email = fields.Email(required=True, error='请输入正确的邮箱', load_only=True)

    @validates('username')
    def validate_username(self, value):
        for c in value:
            if c not in valid_str:
                raise ValidationError('用户名只能使用英文字母、下划线及数字')
        if not (7 < len(value) < 21):
            raise ValidationError('用户名长度(8-20)个英文字符')
        u = User.query.filter_by(username=value).first()
        if u is not None:
            raise ValidationError('用户名已存在')

    @validates('password')
    def validate_password(self, value):
        for c in value:
            if c not in valid_str:
                raise ValidationError('密码只能使用英文字母、下划线及数字')
        if not (7 < len(value) < 21):
            raise ValidationError('密码长度(8-20)个英文字符')

    @validates('confirm')
    def validate_confirm(self, value):
        if value != self.password:
            raise ValidationError('两次输入的密码不一致')

    @validates('email')
    def validate_confirm(self, value):
        u = User.query.filter_by(email=value).first()
        if u is not None:
            raise ValidationError('邮箱已被注册')


register_schema = RegisterSchema()