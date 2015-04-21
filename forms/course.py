#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app,g
from wtforms import Form, validators, TextAreaField
from wtforms import BooleanField, StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length, Regexp,NumberRange
from wtforms.validators import Optional
from models import Student,Account,Course,Xk

class DoxkFrom(Form):
    code = StringField(
        'code', validators=[
            Length(min=0, max=20, message=u"课程代码格式错误")
        ]
    )
    def validate_code(self,field):
        code=field.data
        if Xk.query.filter(Xk.stuid==g.user.username).filter(Xk.code==code).count():
            raise ValueError(u'该课程已选择')
    def save(self):
        choose=Xk(stuid=g.user.username,code=self.code.data)
        choose.save()
        return True

class DotkForm(Form):
    code = StringField(
        'code', validators=[
            Length(min=0, max=20, message=u"课程代码格式错误")
        ]
    )
    def validate_code(self,field):
        code=field.data
        if Xk.query.filter(Xk.stuid==g.user.username).filter(Xk.code==code).count()==0:
            raise ValueError(u'该课程未选择')
    def delete(self):
        kc=Xk.query.filter(Xk.stuid==g.user.username).filter(Xk.code==self.code.data)
        for i in kc:
            i.delete()