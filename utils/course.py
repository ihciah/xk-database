#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import g, request, session, current_app
from flask import url_for, redirect, abort, flash
import functools
import json,sys,os
sys.path.append(os.path.abspath(''))
from models import Student

def gen_course_table(stuid):
    timetable=[[1 for p in range(7)] for t in range(14)]#14*7
    user = Student.query.get(stuid)
    for i in user.courses:
        cname=i.desp
        ccode=i.code
        cplace=i.place
        cteaname=i.teacher.name
        ctime=json.loads(i.time)  #{"1(weekday)":[[1,2],[6,2]]}
        for (weekday,v) in ctime.items():
            for j in v:
                timetable[j[0]-1][int(weekday)-1]=[j[1],cname,cteaname,ccode,cplace] #tt[start_time,weekday]=[last_time,course_name,teacher_name,course_code]
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
            stl.append(str(tj[0])+"-"+str(int(tj[0])+int(tj[1])-1))
        wtime.append(st+','.join(stl))
    return '\r\n'.join(wtime)

def check_if_conflict(allc,sc):
    #参数：所有课程、待选课程
    #返回：1表示冲突，2表示无冲突
    timetable=[[0 for p in range(7)] for k in range(14)]
    for lp in allc:
        k=json.loads(lp.time)
        for i,j in k.items():
            for tj in j:
                timetable[i][i]
