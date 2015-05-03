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
class ProfileForm(Form):
    name = StringField(
        'name', validators=[
            Length(min=0, max=20, message=u"姓名长度必须在20位以下")
        ]
    )
    confirm = PasswordField('confirm')

    password = PasswordField('password', [
        validators.EqualTo('confirm', message=u'两次输入的密码不符')
    ])
    age = IntegerField(
        'age',validators=[
            NumberRange(min=1,max=80, message=u'年龄必须在1~80以内')
        ]
    )
    major = StringField(
        'major', validators=[
            Length(min=0, max=20, message=u"专业长度必须在20位以下")
        ]
    )
    grade = IntegerField(
        'grade',validators=[
            NumberRange(min=2000,max=2020, message=u'年级必须在2000~2020之间')
        ]
    )

    def save(self):
        user = Account.query.get(g.user.username)
        if self.password!='':
            user.password=Account.create_password(self.password)
            user.save()
        stuusr=Student.query.get(g.user.username)
        stuusr.name=self.name.data
        stuusr.age=self.age.data
        stuusr.major=self.major.data
        stuusr.grade=self.grade.data
        stuusr.save()
class SearchForm():
    def __init__(self,r):
        self.scode=r.get('search_course')
    def validate(self):
        if self.scode is not None:
            return True
        return False
    def search(self):
        res=[]#TM给跪了,直接Course.query就是没找到怎么写。。
        sbycode=Course.session.query(Course,func.count(Xk.stuid).label('sum')).join(Xk,Xk.code==Course.code,isouter=True).group_by(Course.code).filter(Course.code.like(self.scode+'%'))
        sr=sbycode.all()
        if len(sr)>0 and sr[0].Course is None:
            sbymajor=Course.session.query(Course,func.count(Xk.stuid).label('sum')).join(Xk,Xk.code==Course.code,isouter=True).group_by(Course.code).filter(Course.major.like(self.scode+'%'))
            sr=sbymajor.all()
            if len(sr)>0 and sr[0].Course is None:
                sbydesp=Course.session.query(Course,func.count(Xk.stuid).label('sum')).join(Xk,Xk.code==Course.code,isouter=True).group_by(Course.code).filter(Course.desp.like(self.scode+'%'))
                sr=sbydesp.all()
        for i in sr:
            if i.Course is not None:
                i.Course.time=transj2w(i.Course.time)
                res.append(i)
        return res
