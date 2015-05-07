#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import g, request, flash
from flask import render_template, redirect
from models import Student,Account,Course,Xk,Teacher,Emp
from forms import SearchStudentFrom,adminProfileForm,UserProfileForm,SearchForm,CourseEditForm,UseraddForm
from utils import get_current_user,require_admin,transt2line,transtea2line,require_teacher,gen_tea_course_table

from models import Account
__all__ = ['bp']

bp = Blueprint('teacher',__name__)
@bp.route('/course-list',methods=['GET'])
@require_teacher
def course_list():
    result=Course.query.join(Emp, Emp.teaid==Course.code==Emp.code).filter(Emp.teaid==g.user.username).all()

@bp.route('/',methods=['GET'])
@require_teacher
def table():
    tt=gen_tea_course_table(g.user.username)
    return render_template('teacher/table.html',timetable=tt)
