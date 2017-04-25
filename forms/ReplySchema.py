from marshmallow import Schema, ValidationError, validates, validate
from marshmallow import fields
from models.Comment import Comment
from models.User import User

class ReplySchema(Schema):
    id = fields.Int(dump_only=True)
    comment_id = fields.Int(required=True, error='评论不存在,刷新后再试')
    content = fields.Str(validate=validate.Length(min=1, max=200, error='内容长度(1-200)个字符'))
    receiver_name = fields.Str(load_only=True, allow_none=True)
    created_time = fields.Time(dump_only=True)

    @validates('comment_id')
    def validate_comment_id(self, value):
        c = Comment.query.get(value)
        if c is None:
            raise ValidationError('评论不存在,刷新后再试')


reply_schema = ReplySchema()