from marshmallow import Schema, ValidationError, validates, validate
from marshmallow import fields
from models.Node import Node
from flask import url_for

class NodeSchema(Schema):
    id = fields.Int(dump_only=True)
    created_time = fields.Time(dump_only=True)
    edited_time = fields.Time(dump_only=True)
    name = fields.Str()
    description = fields.Str(allow_none=True)

    @validates('name')
    def validate_name(self, value):
        if not (2 <= len(value) <= 30):
            raise ValidationError('名字长度(2-30)个字符')
        n = Node.query.find(name=value).first()
        if n is not None:
            raise ValidationError('节点名已存在')

node_schema = NodeSchema()
node_schemas = NodeSchema(many=True)