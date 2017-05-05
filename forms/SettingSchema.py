from marshmallow import Schema, ValidationError, validates, validate
from marshmallow import fields
from flask import url_for
from models.Post import Post
from models.Node import Node
from models.User import User

valid_str = '1234567890_qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'

class SettingSchema(Schema):
    email = fields.Email(required=True, error='请输入正确的邮箱')

    @validates('email')
    def validate_confirm(self, value):
        u = User.query.filter_by(email=value).first()
        if u is not None:
            raise ValidationError('邮箱已被注册')

setting_schema = SettingSchema()