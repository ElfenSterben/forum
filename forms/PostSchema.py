from marshmallow import Schema, ValidationError, validates, validate
from marshmallow import fields
from models.Post import Post
from models.Node import Node
from flask import url_for

class PostSchema(Schema):
    id = fields.Int(dump_only=True)
    created_time = fields.Time(dump_only=True)
    edited_time = fields.Time(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=2, max=200, error='标题长度(2-30)个字符'))
    content = fields.Str(required=True, validate=validate.Length(min=10, max=1000, error='内容长度(10-1000)个字符'))
    node_id = fields.Int(required=True, error='节点类型错误')
    url = fields.Method(dump_only=True)

    def post_url(self, post):
        return url_for('post.view', post_id=post.id)

    @validates('node_id')
    def validate_node_id(self, value):
        n = Node.query.get(value)
        if n is None:
            raise ValidationError('节点不存在')

post_schema = PostSchema()