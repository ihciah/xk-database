#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app,g
from wtforms import Form, validators
from wtforms import BooleanField, StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length, Regexp,NumberRange
from wtforms.validators import Optional
from models import Student,Account,Course,Xk,Kinds,Coursekinds,Majors,Scheme
from sqlalchemy.sql import func
from utils import transj2w
import random

class SearchMajorCourse(Form):
    def __init__(self,r):
        self.majorid=r.get('search_major')
    def validate(self):
        if self.majorid is not None:
            return True
        return False
    def search(self):
        res=[]
        schemes=Scheme.session.query(Scheme).filter(Scheme.majorid == self.majorid).order_by(Scheme.kindid)
        sr1=schemes.all()
        sr1.sort(key=lambda x:len(x.kindid))
        for kind in sr1:
            leftCredit = kind.credit
            schemes = Coursekinds.session.query(Coursekinds,Kinds).filter(Coursekinds.kindid==kind.kindid).filter(Coursekinds.compulsory==1).outerjoin(Kinds,Kinds.kindid==Coursekinds.kindid).limit(int(kind.credit*2))
            sr=schemes.all()
            for i in sr:
                i.addi = len(res)
                i.allcredit = kind.credit
                res.append(i)
                leftCredit -= i.Coursekinds.ccredir
            
            schemes = Coursekinds.session.query(Coursekinds,Kinds).filter(Coursekinds.kindid==kind.kindid).filter(Coursekinds.compulsory==0).outerjoin(Kinds,Kinds.kindid==Coursekinds.kindid).limit(int(kind.credit*2))
            sr=schemes.all()
            sr.sort(key=lambda x:random.random())
            for i in sr:
                if leftCredit <= 0:
                    break
                i.addi = len(res)
                i.allcredit = kind.credit
                res.append(i)
                leftCredit -= i.Coursekinds.ccredir

        return res
        
        
class SearchMajorid(Form):
    def __init__(self,r):
        self.majorid=r.get('search_major')
    def validate(self):
        if self.majorid is not None:
            return True
        return False
    def search(self):
        res=[]#TM给跪了,直接Course.query就是没找到怎么写。。
        #sbycode=Course.session.query(Course,func.count(Xk.stuid).label('sum')).outerjoin(Xk,Xk.code==Course.code).group_by(Course.code).filter(Course.code.like(self.scode+'%'))
        
        schemes=Majors.session.query(Majors).filter(Majors.majorname.like('%'+self.majorid+'%'))
        sr1=schemes.all()
        for i in sr1:
            res.append(i)
        schemes=Majors.session.query(Majors).filter(Majors.majorid.like('%'+self.majorid+'%'))
        sr1=schemes.all()
        for i in sr1:
            res.append(i)
        return res
