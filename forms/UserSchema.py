from marshmallow import Schema, ValidationError, validates, validate
from marshmallow import fields
from models.Post import Post
from models.Node import Node
from models.User import User

valid_str = '1234567890_qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    avatar = fields.Str(dump_only=True)
    email = fields.Email(required=True, error='邮箱格式错误')
    created_time = fields.Time(dump_only=True)

    @validates('username')
    def validate_username(self, value):
        for c in value:
            if c not in valid_str:
                raise ValidationError('用户名只能使用英文字母、下划线及数字')
        if not (7 < len(value) < 21):
            raise ValidationError('用户名长度(8-20)个英文字符')

    @validates('password')
    def validate_password(self, value):
        for c in value:
            if c not in valid_str:
                raise ValidationError('密码只能使用英文字母、下划线及数字')
        if not (7 < len(value) < 21):
            raise ValidationError('密码长度(8-20)个英文字符')


user_schema = UserSchema()