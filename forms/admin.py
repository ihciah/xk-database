#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app,g
from wtforms import Form, validators
from wtforms import BooleanField, StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length, Regexp,NumberRange
from wtforms.validators import Optional
from models import Student,Account,Course,Xk
from sqlalchemy.sql import func
from utils import transj2w

class SearchStudentFrom(Form):
    stuid = StringField(
        'stuid', validators=[
            Length(min=0, max=20, message=u"学生id格式错误")
        ]
    )
    name = StringField(
        'sname', validators=[
            Length(min=0, max=20, message=u"学生姓名格式错误")
        ]
    )

    def dosearch(self):
        if self.stuid.data is None and self.name.data is None:
            raise ValueError(u'用户名和学生id至少填写一个!')
        result=Student.query
        if self.stuid.data is not None and self.stuid.data!='':
            result=result.filter(Student.stuid.like(self.stuid.data+'%'))
        if self.name.data is not None and self.name.data!='':
            result=result.filter(Student.name.like(self.name.data+'%'))
        return result.all()


class adminProfileForm(Form):
    confirm = PasswordField('confirm')
    password = PasswordField('password', [
        validators.EqualTo('confirm', message=u'两次输入的密码不符'),
        validators.Length(min=1, max=20, message=u"密码长度需在1~20位之间")
    ])

    def save(self):
        user = Account.query.get(g.user.username)
        if self.password!='':
            user.password=Account.create_password(self.password)
            user.save()