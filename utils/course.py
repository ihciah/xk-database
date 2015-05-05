#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json,sys,os
sys.path.append(os.path.abspath(''))
from flask import g, request, session, current_app
from flask import url_for, redirect, abort, flash
import functools
from sqlalchemy.sql import func
from models import Student,Course,Xk
import random

def gen_course_table(stuid):
    timetable=[[1 for p in range(7)] for t in range(14)]#14*7
    user = Student.query.get(stuid)
    colors=['red','blue','yellow','green','#00FFFF','black','white','#FE2EF7','#FF8000','#4C0B5F','#A9F5A9','#F7819F']
    random.shuffle(colors)
    count=0
    for i in user.courses:
        count=count+1
        cname=i.desp
        ccode=i.code
        cteaname=''
        for te in i.teacher:
            cteaname+=te.name+' '
        for time in i.ctime:
            timetable[time.starttime-1][time.weekday-1]=[time.durtime,cname,cteaname,ccode,time.place,time.additional,colors[count%(len(colors))]]
            for j in range(time.starttime,time.starttime+time.durtime):
                timetable[j][time.weekday-1]=0
    return timetable

def transj2w(times):
    tra={'1':u'周一',
         '2':u'周二',
         '3':u'周三',
         '4':u'周四',
         '5':u'周五',
         '6':u'周六',
         '7':u'周日'
    }
    wtime=[]
    for time in times:
        wtime.append("%s %d-%d@%s%s" %(tra[str(time.weekday)],time.starttime,time.durtime+time.starttime-1,time.place,time.additional))
    return '\r\n'.join(wtime)

def check_if_conflict(allc,sc):
    #参数：所有课程列表、待选课程
    #返回：1表示冲突，0表示无冲突
    timetable=[[0 for p in range(7)] for k in range(14)]#14*7
    for lp in allc:
        mk=lp.ctime
        for k in mk:
            for i in range(k.starttime,k.starttime+k.durtime):
                timetable[i-1][k.weekday-1]=1
    mk=sc.ctime
    for k in mk:
        for i in range(k.starttime,k.starttime+k.durtime):
            if timetable[i-1][k.weekday-1]==1:
                return 1
    return 0

def check_if_full(cid):
    #已满=1  可选=0
    num_limit=Course.query.get(cid).num
    num_already=Xk.query.filter(Xk.code==cid).count()
    if num_already>=num_limit:
        return 1
    return 0

def get_credit(sid):
    #学号->学分
    x=Course.session.query(func.sum(Course.credit).label('sum')).join(Xk, Xk.code==Course.code).filter(Xk.stuid==sid)
    return x[0].sum or 0

def get_people_count(cid):
    #类似check_if_full
    num_limit=Course.query.get(cid).num
    num_already=Xk.query.filter(Xk.code==cid).count()
    return {'now':num_already,'max':num_limit}

