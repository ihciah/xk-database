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
import random

class SearchMajorCourse(Form):
    def __init__(self,r):
        self.scode=r.get('search_major')
    def validate(self):
        if self.scode is not None:
            return True
        return False
    def search(self):
        res=[]#TM给跪了,直接Course.query就是没找到怎么写。。
        sbycode=Course.session.query(Course,func.count(Xk.stuid).label('sum')).outerjoin(Xk,Xk.code==Course.code).group_by(Course.code).filter(Course.code.like(self.scode+'%'))
        sr=sbycode.all()
        if len(sr)==0 or (len(sr)>0 and sr[0].Course is None):
            sbymajor=Course.session.query(Course,func.count(Xk.stuid).label('sum')).outerjoin(Xk,Xk.code==Course.code).group_by(Course.code).filter(Course.major.like(self.scode+'%'))
            sr=sbymajor.all()
            if len(sr)==0 or (len(sr)>0 and sr[0].Course is None):
                sbydesp=Course.session.query(Course,func.count(Xk.stuid).label('sum')).outerjoin(Xk,Xk.code==Course.code).group_by(Course.code).filter(Course.desp.like(self.scode+'%'))
                sr=sbydesp.all()
        for i in sr:
            if i.Course is not None:
                i.time=transj2w(i.Course.ctime)
                #setattr( i.Course.__class__, 'time', transj2w(i.Course.ctime))
                res.append(i)
        return res
