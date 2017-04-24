from marshmallow import Schema, ValidationError, validates, validate
from marshmallow import fields
from flask import url_for
from models.Post import Post
from models.Node import Node
from models.User import User

valid_str = '1234567890_qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    confirm=fields.Str(required=True, load_only=True)
    avatar = fields.Str(dump_only=True)
    email = fields.Email(required=True, error='请输入正确的邮箱')
    created_time = fields.Time(dump_only=True)
    url = fields.Method(method_name='user_url', dump_only=True)

    def user_url(self, user):
        return url_for('user.info_view', username=user.username)

    @validates('username')
    def validate_username(self, value):
        for c in value:
            if c not in valid_str:
                raise ValidationError('用户名只能使用英文字母、下划线及数字')
        if not (7 < len(value) < 21):
            raise ValidationError('用户名长度(8-20)个英文字符')
        u = User.query.filter_by(username=value).first()
        if u is None:
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


user_schema = UserSchema()