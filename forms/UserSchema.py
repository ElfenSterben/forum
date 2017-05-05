from marshmallow import Schema, ValidationError, validates, validate
from marshmallow import fields
from flask import url_for
from models.Post import Post
from models.Node import Node
from models.User import User

valid_str = '1234567890_qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(allow_none=True)
    avatar = fields.Str(dump_only=True)
    password = fields.Str(required=True, load_only=True)
    created_time = fields.Time(dump_only=True)
    url = fields.Method(method_name='user_url', dump_only=True)

    def user_url(self, user):
        return url_for('user.info_view', username=user.username)

user_schema = UserSchema()