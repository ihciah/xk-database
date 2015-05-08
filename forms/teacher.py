#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app,g
from wtforms import Form, validators
from wtforms import BooleanField, StringField, PasswordField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length, Regexp,NumberRange
from wtforms.validators import Optional
from models import Student,Account,Course,Xk,Teacher,Timeplace,Emp
from sqlalchemy.sql import func
from utils import check_if_conflict,check_if_full,transtea2line,transline2tea,transline2times

class SetScoreForm(Form):
    code = StringField(
        'code', validators=[
            Length(min=0, max=20, message=u"课程代码格式错误")
        ]
    )
    stuid = StringField(
        'stuid', validators=[
            Length(min=0, max=20, message=u"学生ID格式错误")
        ]
    )
    score = FloatField(
        'score',validators=[
            NumberRange(min=0,max=100, message=u'分数必须在0~100以内')
        ]
    )
    def validate_code(self,field):
        code=field.data
        if Xk.query.filter(Xk.stuid==self.stuid.data).filter(Xk.code==code).count()==0:
            raise ValueError(u'该生未选择该课程')
    def set(self):
        cour=Xk.query.filter(Xk.stuid==self.stuid.data).filter(Xk.code==self.code.data).first()
        cour.score=self.score.data
        cour.save()
        return True

class stuaddForm(Form):
    code = StringField(
        'code', validators=[
            Length(min=1, max=20, message=u"课程代码格式错误")
        ]
    )
    stuid = StringField(
        'stuid', validators=[
            Length(min=1, max=20, message=u"学生ID格式错误")
        ]
    )
    def validate_code(self,field):
        code=field.data
        if Xk.query.filter(Xk.stuid==self.stuid.data).filter(Xk.code==code).count()!=0:
            raise ValueError(u'该生已选择过该课程')
        else:
            if Emp.query.filter(Emp.teaid==g.user.username).filter(Emp.code==code).count==0:
                raise ValueError(u'因为你并不属于该课程任课教师，所以你无权选择修改课程学生')
    def validate_stuid(self,field):

        if Student.query.get(field.data) is None:
            raise ValueError(u'该学生不存在!')
        else:
        #验证时间是否冲突
            sc=Course.query.get(self.code.data)
            allc=Course.query.join(Xk, Xk.code==Course.code).filter(Xk.stuid==self.stuid.data)
            if check_if_conflict(allc,sc):
                raise ValueError(u'该课程与学生当前课程时间冲突!')
    def save(self):
        x=Xk(code=self.code.data,stuid=self.stuid.data)
        x.save()