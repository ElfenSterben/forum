from marshmallow import Schema, ValidationError, validates, validate
from marshmallow import fields
from models.Post import Post


class CommentSchema(Schema):
    id = fields.Int(dump_only=True)
    created_time = fields.Raw(dump_only=True)
    edited_time = fields.Raw(dump_only=True)
    content = fields.Str(validate=validate.Length(min=1, max=200, error='内容长度(1-200)个字符'))
    post_id = fields.Int(required=True, error='主题不存在')

    @validates('post_id')
    def validate_post_id(self, value):
        p = Post.query.get(value)
        if p is None:
            raise ValidationError('主题不存在')

comment_schema = CommentSchema()