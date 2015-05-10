#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _base import *

class Kinds(db.Model,SessionMixin):
    __tablename__ = "kinds" #课程种类和描述
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_general_ci'
    }
    kindid = db.Column(db.String(50), primary_key=True, nullable=False)#课程种类id
    '''
    C.COM.1:公共必修课(1类核心课程)
    C.OPT.1:公共选修课(2类核心课程)
    COMP.COM.1:专业必修课(包括基础课)
    COMP.OPT.1:专业选修课
    '''
    kindname = db.Column(db.String(100), primary_key=False, nullable=True)#种类说明

class Coursekinds(db.Model,SessionMixin):
    __tablename__ = "coursekinds"#课程的种类
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_general_ci'
    }
    code = db.Column(db.String(100), primary_key=True, nullable=False)#课程代码(不完整版)
    coursename = majorname = db.Column(db.String(100),nullable=True)#课程名称
    ccredir = db.Column(db.Float(precision=1), default=0)#这门课的学分
    kindid = db.Column(db.String(50), ForeignKey('kinds.kindid'), nullable=False, primary_key=True)#课程种类id
    compulsory = db.Column(db.Integer, default=0)#1->必修;0->选修
    semester = db.Column(db.Integer, default=0)#推荐修读学期(0-8)，0为无
    kinds = relationship('kinds')
    
class Majors(db.Model,SessionMixin):
    __tablename__ = "majors"#专业代码和描述
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_general_ci'
    }
    majorid = db.Column(db.String(50), primary_key =True, nullable=False)#专业代码,like:COMP1
    majorname = db.Column(db.String(50),nullable=True)
    
    
class Scheme(db.Model,SessionMixin):
    __tablename__ = "scheme"#培养方案
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_general_ci'
    }
    majorid = db.Column(db.String(100), ForeignKey('majors.majorid'), nullable=False, primary_key=True)
    kindid = db.Column(db.String(50), ForeignKey('kinds.kindid'), nullable=False, primary_key=True)
    credit = db.Column(db.Float(precision=1), default=0)#要修读的学分
    majors = relationship('Majors')
    kinds = relationship('Kinds')
    coursekinds = relationship('Coursekinds')
    
    