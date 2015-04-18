#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app
from wtforms import Form, validators, TextAreaField
from wtforms import BooleanField, StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length, Regexp,NumberRange
from wtforms.validators import Optional
from models import Account
class SignupForm(Form):
    username = StringField(
        'username', validators=[
            DataRequired(message=u"学号不能为空")
        ], description='only numbers!(1-12)',
    )

    confirm = PasswordField('confirm')

    password = PasswordField('password', [
        validators.DataRequired(message=u"密码不能为空"),
        validators.EqualTo('confirm', message=u'两次输入的密码不符')
    ])

    def validate_username(self, field):
        data = field.data
        if Account.query.filter_by(username=data).count():
            raise ValueError(u'此用户名已被注册')

    def save(self, role=1):
        user = Account(**self.data)
        user.role=role
        user.save()
        return user


class SigninForm(Form):
    username = IntegerField('username', [validators.Length(min=1, max=20)])
    password = PasswordField('password', [validators.DataRequired()])

    def validate_password(self, field):
        username = self.username.data
        user = Account.query.filter_by(username=username).first()
        if not user:
            raise ValueError(u'用户不存在')
        if user.check_password(field.data):
            self.user = user
            return user
        raise ValueError(u'用户名密码不匹配')