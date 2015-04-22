#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app,g
from wtforms import Form, validators, TextAreaField
from wtforms import BooleanField, StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length, Regexp,NumberRange
from wtforms.validators import Optional
from models import Student,Account,Course,Xk
from utils import check_if_conflict,check_if_full,get_people_count

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
        #check if time conflict
        allcourses=Course.query.join(Xk, Course.code==Xk.code).filter(Xk.stuid==g.user.username).all()
        selectcourse=Course.query.filter(Course.code==code).first()
        if not selectcourse:
            raise ValueError(u'该课程不存在')
        ####TO########
        #时间冲突判断--ok
        #人数是否满判断
        if check_if_conflict(allcourses,selectcourse):
            raise ValueError(u'时间冲突')
        if check_if_full(code):
            raise ValueError(u'人数已满')
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

class Get_count(Form):
    cid = StringField(
        'cid', validators=[
            Length(min=1, max=30, message=u"选课号长度错误")
        ]
    )
    def get_res(self):
        return get_people_count(self.cid.data)