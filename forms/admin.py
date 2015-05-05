#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app,g
from wtforms import Form, validators
from wtforms import BooleanField, StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length, Regexp,NumberRange
from wtforms.validators import Optional
from models import Student,Account,Course,Xk,Teacher
from sqlalchemy.sql import func
from utils import transj2w

class SearchStudentFrom(Form):
    stuid = StringField(
        'stuid', validators=[
            Length(min=0, max=20, message=u"用户ID格式错误")
        ]
    )
    sname = StringField(
        'sname', validators=[
            Length(min=0, max=20, message=u"用户姓名格式错误")
        ]
    )

    def dosearch(self):
        res_stu=Student.query
        res_tea=Teacher.query
        current_app.logger.debug(self.sname.data)
        if self.stuid.data is not None and self.stuid.data.replace(' ','')!='':
            self.stuid.data = self.stuid.data.replace('%','').replace(' ','')
            res_stu=res_stu.filter(Student.stuid.like(self.stuid.data+'%'))
            res_tea=res_tea.filter(Teacher.teaid.like(self.stuid.data+'%'))
        if self.sname.data is not None and self.sname.data.replace(' ','')!='':
            self.sname.data = self.sname.data.replace('%','').replace(' ','')
            res_stu=res_stu.filter(Student.name.like(self.sname.data+'%'))
            res_tea=res_tea.filter(Teacher.name.like(self.sname.data+'%'))
        return res_stu.all(),res_tea.all()


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