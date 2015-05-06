#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app,g
from wtforms import Form, validators
from wtforms import BooleanField, StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length, Regexp,NumberRange
from wtforms.validators import Optional
from models import Student,Account,Course,Xk,Teacher
from sqlalchemy.sql import func
from utils import check_if_conflict,check_if_full

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

class UserProfileForm(Form):
    stuid = StringField(
        'stuid', validators=[
            Length(min=0, max=20, message=u"学号长度必须在20位以下")
        ]
    )
    teaid = StringField(
        'teaid', validators=[
            Length(min=0, max=20, message=u"教师编号长度必须在20位以下")
        ]
    )
    uname = StringField(
        'uname', validators=[
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
    sex = IntegerField(
        'sex',validators=[
            NumberRange(min=0,max=2, message=u'请选择性别')
        ]
    )
    major = StringField(
        'major', validators=[
            Length(min=0, max=20, message=u"专业长度必须在20位以下")
        ]
    )
    grade = IntegerField('grade')
    def save(self):
        user=None
        uid='1'
        type=0
        if self.stuid.data is not None and self.stuid.data!='':
            user = Student.query.get(self.stuid.data)
            uid=self.stuid.data
            type=1
        if self.teaid.data is not None and self.teaid.data!='':
            user = Teacher.query.get(self.teaid.data)
            uid=self.teaid.data
            type=2
        if user is None:
            return
        self.type=type
        if self.password!='':
            accuser = Account.query.get(uid)
            if accuser is not None:
                accuser.password=Account.create_password(self.password)
                accuser.save()
        if type==1:
            user.name=self.uname.data
            user.age=self.age.data
            user.sex=self.sex.data
            user.major=self.major.data
            user.grade=self.grade.data
        else:
            user.name=self.uname.data
            user.age=self.age.data
            user.sex=self.sex.data
            user.major=self.major.data
        user.save()

class adminDoxkForm(Form):
    stuid = StringField(
        'stuid', validators=[
            Length(min=1, max=20, message=u"学生代码格式错误")
        ]
    )
    code = StringField(
        'code', validators=[
            Length(min=1, max=20, message=u"选课代码格式错误")
        ]
    )
    def validate_code(self,field):
        code=field.data
        if Xk.query.filter(Xk.stuid==self.stuid.data).filter(Xk.code==code).count():
            raise ValueError(u'该课程已选择')
        #check if time conflict
        allcourses=Course.query.join(Xk, Course.code==Xk.code).filter(Xk.stuid==self.stuid.data).all()
        selectcourse=Course.query.filter(Course.code==code).first()
        if not selectcourse:
            raise ValueError(u'该课程不存在')
        ####TO########
        #时间冲突判断--ok
        #人数是否满判断
        if check_if_conflict(allcourses,selectcourse):
            raise ValueError(u'时间冲突')
        #if check_if_full(code):
        #    raise ValueError(u'人数已满')
        #管理员可在人数超过限定人数的情况下添加课程
    def save(self):
        choose=Xk(stuid=self.stuid.data,code=self.code.data)
        choose.save()
        return True

class adminDotkForm(Form):
    stuid = StringField(
        'stuid', validators=[
            Length(min=1, max=20, message=u"学生代码格式错误")
        ]
    )
    code = StringField(
        'code', validators=[
            Length(min=1, max=20, message=u"选课代码格式错误")
        ]
    )
    def validate_code(self,field):
        code=field.data
        if Xk.query.filter(Xk.stuid==self.stuid.data).filter(Xk.code==code).count()==0:
            raise ValueError(u'该课程未选择!')
    def delete(self):
        kc=Xk.query.filter(Xk.stuid==self.stuid.data).filter(Xk.code==self.code.data)
        for i in kc:
            i.delete()