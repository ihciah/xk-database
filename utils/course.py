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
        cteaname=i.teacher.name
        ctime=json.loads(i.time)  #{"1(weekday)":[[1,2],[6,2]]}
        for (weekday,v) in ctime.items():
            for j in v:
                timetable[j[0]-1][int(weekday)-1]=[j[1],cname,cteaname,ccode] #tt[start_time,weekday]=[last_time,course_name,teacher_name,course_code]
                for co in range(j[0]+1,j[0]+j[1]):
                    timetable[co-1][int(weekday)-1]=0
    return timetable


