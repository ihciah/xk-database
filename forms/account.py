#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app
from wtforms import Form, validators, TextAreaField
from wtforms import BooleanField, StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length, Regexp,NumberRange
from wtforms.validators import Optional
from models import Account,Student
class SignupForm(Form):
    username = StringField(
        'username', validators=[
            DataRequired(message=u"学号不能为空"),
            Length(min=1, max=20, message=u"长度必须在1-20位之间")
        ], description='only numbers!(1-12)',
    )

    confirm = PasswordField('confirm')

    password = PasswordField('password', [
        validators.DataRequired(message=u"密码不能为空"),
        validators.EqualTo('confirm', message=u'两次输入的密码不符')
    ])

    def validate_username(self, field):
        data = field.data
        if Account.query.get(data):
            raise ValueError(u'此用户名已被注册')

    def save(self, role=1):
        user = Account(**self.data)
        user.role=role
        user.save()
        stuusr=Student(stuid=user.username,grade="20"+user.username[0:2])
        stuusr.save()
        return user


class LoginForm(Form):
    username = StringField('username', [validators.Length(min=1, max=20, message=u"长度必须在1-20位之间")])
    password = PasswordField('password', [validators.DataRequired(message=u"请输入密码")])

    def validate_password(self, field):
        username = self.username.data
        user = Account.query.get(username)
        if not user:
            raise ValueError(u'用户不存在')
        if user.check_password(field.data):
            self.user = user
            return user
        raise ValueError(u'用户名密码不匹配')