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
        if self.password.data!='':
            user.password=Account.create_password(self.password.data)
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
    prof = StringField(
        'prof', validators=[
            Length(min=0, max=20, message=u"职称长度必须在20位以下")
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
        if self.password.data!='':
            accuser = Account.query.get(uid)
            if accuser is not None:
                accuser.password=Account.create_password(self.password.data)
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
            user.prof=self.prof.data
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

class CourseEditForm(Form):
    code = StringField(
        'code', validators=[
            Length(min=1, max=20, message=u"课程代码长度错误")
        ]
    )
    desp = StringField(
        'desp', validators=[
            Length(min=1, max=20, message=u"课程名长度错误")
        ]
    )
    major = StringField(
        'major', validators=[
            Length(min=0, max=20, message=u"选课院系长度错误")
        ]
    )
    additional=StringField(
        'additional', validators=[
            Length(min=0, max=20, message=u"额外信息长度错误")
        ]
    )
    num = IntegerField(
        'num',validators=[
            NumberRange(min=1,max=10000, message=u'人数限制格式错误')
        ]
    )
    credit = FloatField('credit')
    coursetime=StringField('coursetime')
    teas=StringField('teas')

    def validate_teas(self,field):
        tea=transline2tea(field.data)
        for i in tea:
            if not Teacher.query.get(i):
                raise ValueError(u'教师编号%s不存在!' %i)
    def validate_coursetime(self,field):
        t=transline2times(self.coursetime.data)
        if t is None or t==False:
            raise ValueError(u'时间格式不正确!')

    def save(self):
        cour=Course.query.get(self.code.data)
        if cour is None:
            cour=Course(code=self.code.data,desp=self.desp.data,major=self.major.data,additional=self.additional.data,num=self.num.data,credit=self.credit.data)
        else:
            cour.modify(code=self.code.data,desp=self.desp.data,major=self.major.data,additional=self.additional.data,num=self.num.data,credit=self.credit.data)
        cour.save()
        t=transline2times(self.coursetime.data)
        if t!=False and t is not None and len(t)!=0:
            cdel=Timeplace.query.filter(Timeplace.code == self.code.data)
            cdel.delete()
            for st in t:
                ta=Timeplace(code=self.code.data,weekday=st[0],starttime=st[1],durtime=st[2],place=st[3])
                ta.save()
        tea=transline2tea(self.teas.data)
        if tea is not None and len(tea)!=0:
            tdel=Emp.query.filter(Emp.code==self.code.data)
            tdel.delete()
            for st in tea:
                ta=Emp(code=self.code.data,teaid=st)
                ta.save()
        return cour
class UseraddForm(Form):
    username = StringField(
        'username', validators=[
            DataRequired(message=u"学号不能为空"),
            Length(min=1, max=20, message=u"长度必须在1-20位之间")
        ], description='only numbers!(1-12)',
    )
    role = IntegerField(
        'role',validators=[
            NumberRange(min=1,max=3, message=u'权限设置错误!')
        ]
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

    def save(self):
        user = Account(**self.data)
        user.save()
        if self.role.data==1:
            stuusr=Student(stuid=self.username.data)
            stuusr.save()
        if self.role.data==3:
            teausr=Teacher(teaid=self.username.data)
            teausr.save()

        return self.username.data,self.role.data

class DelCourseForm(Form):
    code = StringField(
        'code', validators=[
            Length(min=1, max=20, message=u"选课代码格式错误")
        ]
    )
    def validate_code(self,field):
        code=field.data
        if Course.query.get(field.data) is None:
            raise ValueError(u'该课程不存在!')

    def delete(self):
        kc=Xk.query.filter(Xk.code==self.code.data)
        for i in kc:
            i.delete()
        kt=Emp.query.filter(Emp.code==self.code.data)
        for i in kt:
            i.delete()
        ktm=Timeplace.query.filter(Timeplace.code==self.code.data)
        for i in ktm:
            i.delete()
        p=Course.query.get(self.code.data)
        p.delete()
class DelUserForm(Form):
    username = StringField(
        'username', validators=[
            Length(min=1, max=20, message=u"选课代码格式错误")
        ]
    )
    def validate_username(self,field):
        u=Account.query.get(field.data)
        if u is None:
            raise ValueError(u'该用户不存在!')
        else:
            if u.role == 2:
                raise ValueError(u'该用户为管理员用户,不允许删除!')
    def delquery(self,q):
        for i in q:
            i.delete()
    def delete(self):
        self.delquery(Xk.query.filter(Xk.stuid==self.username.data))
        self.delquery(Emp.query.filter(Emp.code==self.username.data))
        self.delquery(Teacher.query.filter(Teacher.teaid==self.username.data))
        self.delquery(Student.query.filter(Student.stuid==self.username.data))
        self.delquery(Account.query.filter(Account.username==self.username.data))