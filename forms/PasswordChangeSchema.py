from marshmallow import Schema, ValidationError, validates, validate
from marshmallow import fields
from flask import g

valid_str = '1234567890_qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'

class PwdChangeSchema(Schema):
    old_password = fields.Str()
    new_password = fields.Str()
    confirm_password = fields.Str()

    @validates('old_password')
    def validate_password(self, value):
        if value != g.user.password:
            raise ValidationError('原密码错误')

    @validates('new_password')
    def validate_new_password(self, value):
        valid = True
        for c in value:
            if c not in valid_str:
                valid = False
                break
        if not (7 < len(value) < 21):
            valid = False
        if not valid:
            raise ValidationError('请输入8-20位密码,只能使用英文字母、下划线及数字')

    @validates('confirm_password')
    def validate_confirm(self, value):
        if value != self.new_password:
            raise ValidationError('两次输入的密码不一致')

pwd_change_schema = PwdChangeSchema()