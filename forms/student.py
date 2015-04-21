#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app,g
from wtforms import Form, validators, TextAreaField
from wtforms import BooleanField, StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length, Regexp,NumberRange
from wtforms.validators import Optional
from models import Student,Account,Course
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
    age=IntegerField(
        'age',validators=[
            NumberRange(min=1,max=80, message=u'年龄必须在1~80以内')
        ]
    )
    major = StringField(
        'major', validators=[
            Length(min=0, max=20, message=u"专业长度必须在20位以下")
        ]
    )
    grade=IntegerField(
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
class SearchForm(Form):
    name = StringField(
        'search', validators=[
            Length(min=0, max=20, message=u"搜索关键字必须在0字以上20字以下")
        ]
    )
    def search(self):
        res=[]
        sbycode=Course.query.filter(Course.code.like(self.name.data+'%'))
        sbymajor=Course.query.filter(Course.major==self.name.data)
        sr=sbycode.union(sbymajor).all()
        for i in sr:
            i.time=transj2w(i.time)
            current_app.logger.debug(i.time)
            res.append(i)

        #sbyteacher=Course.query.filter(Course.teacher.name.like('%'+self.name.data+'%')).all()
        #res=res+[i for i in sbyteacher]
        return res
