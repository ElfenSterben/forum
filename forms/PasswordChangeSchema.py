from marshmallow import Schema, ValidationError, validates, validates_schema, validate
from marshmallow import fields
from flask import g
from utils.utils import is_ulalnum, check_len

class PasswordChangeSchema(Schema):
    old_password = fields.Str()
    new_password = fields.Str()
    confirm_password = fields.Str()

    @validates_schema
    def validate_change_password(self, data):
        old_pwd = data['old_password']
        new_pwd = data['new_password']
        confirm_pwd = data['confirm_password']
        if old_pwd != g.user.password:
            raise ValidationError('原密码错误', 'old_password')
        valid = self.validate_new_pwd(new_pwd)
        if not valid:
            raise ValidationError('请输入8-20位密码,只能使用英文字母、下划线及数字', 'new_password')
        if new_pwd != confirm_pwd:
            raise ValidationError('两次输入的密码不一致', 'confirm_password')

    def validate_new_pwd(self, value):
        law_valid = is_ulalnum(value)
        len_valid = check_len(value, 8, 20)
        return law_valid and len_valid

pwd_change_schema = PasswordChangeSchema()