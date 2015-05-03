#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json,sys,os
sys.path.append(os.path.abspath(''))
from flask import g, request, session, current_app
from flask import url_for, redirect, abort, flash
import functools
from sqlalchemy.sql import func
from models import Student,Course,Xk

def gen_course_table(stuid):
    timetable=[[1 for p in range(7)] for t in range(14)]#14*7
    user = Student.query.get(stuid)
    for i in user.courses:
        cname=i.desp
        ccode=i.code
        #cteaname=i.teacher.name
        cteaname=''
        for te in i.teacher:
            cteaname+=te.name+' '
        ctime=json.loads(i.time)  #{"1(weekday)":[[1,2],[6,2]]}  UPDATE:{"1(weekday)":[[1,2,'Z2101'],[6,2,'Z2212']]}
        for (weekday,v) in ctime.items():
            for j in v:
                timetable[j[0]-1][int(weekday)-1]=[j[1],cname,cteaname,ccode,j[2]] #tt[start_time,weekday]=[last_time,course_name,teacher_name,course_code,classroom]
                for co in range(j[0]+1,j[0]+j[1]):
                    timetable[co-1][int(weekday)-1]=0
    return timetable

def transj2w(js):
    tra={'1':u'周一',
         '2':u'周二',
         '3':u'周三',
         '4':u'周四',
         '5':u'周五',
         '6':u'周六',
         '7':u'周日'
    }
    k=json.loads(js)
    wtime=[]
    for i,j in k.items():
        st=tra[str(i)]+" "
        stl=[]
        for tj in j:
            stl.append(str(tj[0])+"-"+str(int(tj[0])+int(tj[1])-1)+'@'+tj[2])
        wtime.append(st+','.join(stl))
    return '\r\n'.join(wtime)

def check_if_conflict(allc,sc):
    #参数：所有课程列表、待选课程
    #返回：1表示冲突，0表示无冲突
    timetable=[[0 for p in range(7)] for k in range(14)]#14*7
    for lp in allc:
        k=json.loads(lp.time)
        for i,j in k.items():
            #i表示星期几
            for tj in j:
                #tj[0]表示开始时间,tj[1]表示持续时间
                for f in range(int(tj[0]),int(tj[0])+int(tj[1])):
                    timetable[int(f)][int(i)]=1
    k=json.loads(sc.time)
    for i,j in k.items():
        for tj in j:
            for f in range(int(tj[0]),int(tj[0])+int(tj[1])):
                if timetable[int(f)][int(i)]==1:
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
    return x[0].sum

def get_people_count(cid):
    #类似check_if_full
    num_limit=Course.query.get(cid).num
    num_already=Xk.query.filter(Xk.code==cid).count()
    return {'now':num_already,'max':num_limit}

