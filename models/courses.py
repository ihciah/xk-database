#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _base import *

class Student(db.Model, SessionMixin):
    __tablename__ = "students"
    stuid = db.Column(db.String(100),primary_key=True, nullable=False)
    name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    sex = db.Column(db.Integer)#1->Male;0->Female
    major = db.Column(db.String(50))
    grade = db.Column(db.Integer)
    courses = relationship(
        'Course',
        secondary='xks'
    )

class Course(db.Model, SessionMixin):
    __tablename__ = "courses"
    code = db.Column(db.String(100), primary_key=True, nullable=False)#选课代码
    num = db.Column(db.Integer,nullable=False)#限制人数
    desp = db.Column(db.String(200))#课程名
    addi_desp = db.Column(db.String(400),default='')#额外说明，如不允许其中退课，双周上课，1-9周上课等
    major = db.Column(db.String(50))#开课院系
    time = db.Column(db.String(500))#时间（json格式，见utils）
    credit = db.Column(db.Float(precision=1), default=0)
    students = relationship(
        'Student',
        secondary='xks'
    )
    teacher=relationship(
        'Teacher',
        secondary='emp'
    )
    xk=relationship('Xk')

class Xk(db.Model, SessionMixin):
    __tablename__ = "xks"
    code = db.Column(db.String(100), ForeignKey('courses.code'), nullable=False, primary_key=True)
    stuid = db.Column(db.String(100), ForeignKey('students.stuid'), nullable=False, primary_key=True)

class Teacher(db.Model, SessionMixin):
    __tablename__ = "teachers"
    teaid = db.Column(db.String(100), primary_key=True, nullable=False)#教师id
    name = db.Column(db.String(50))#教师姓名
    prof = db.Column(db.String(50))#职称
    major = db.Column(db.String(50))#院系
    age = db.Column(db.Integer)#年龄
    sex = db.Column(db.Integer)#1->Male;0->Female
    courses = relationship(
        'Course',
        secondary='emp'
    )

class Emp(db.Model, SessionMixin):
    __tablename__ = "emp"
    code = db.Column(db.String(100), ForeignKey('courses.code'), nullable=False, primary_key=True)
    teaid = db.Column(db.String(100), ForeignKey('teachers.teaid'), nullable=False, primary_key=True)