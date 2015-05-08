#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import g, request, flash
from flask import render_template, redirect
from models import Student,Account,Course,Xk,Teacher,Emp
from forms import SearchStudentFrom,adminProfileForm,UserProfileForm,SearchForm,CourseEditForm,UseraddForm, stuaddForm
from utils import get_current_user,require_admin,transt2line,transtea2line,require_teacher,gen_tea_course_table

from models import Account
__all__ = ['bp']

bp = Blueprint('teacher',__name__)


@bp.route('/course-list',methods=['GET'])
@require_teacher
def course_list():
    result=Course.query.join(Emp, Course.code==Emp.code).filter(Emp.teaid==g.user.username).all()
    return render_template('teacher/courselist.html',result=result)

@bp.route('/',methods=['GET'])
@require_teacher
def table():
    tt=gen_tea_course_table(g.user.username)
    return render_template('teacher/table.html',timetable=tt)

@bp.route('/stulist',methods=['GET','POST'])
@require_teacher
def stulist():
    if request.method == 'GET':
        coursecode=request.args.get('course')
        if coursecode is None or coursecode=='':
            return render_template('teacher/search_stu.html')
        #验证课程代码是否有该教师id
        if Emp.query.filter(Emp.teaid==g.user.username).filter(Emp.code==coursecode).count()==0:
            return redirect("/teacher/stulist")
        students=Student.session.query(Student,Xk).join(Xk, Xk.stuid==Student.stuid).filter(Xk.code==coursecode).all()
        return render_template('teacher/search_stu_result.html',courseid=coursecode,result=students)
    #根据POST数据查询学生(待写)

@bp.route('/stuadd',methods=['GET','POST'])
@require_teacher
def stuadd():
    if request.method == 'GET':
        return render_template('teacher/add_stu.html')
    form=stuaddForm(request.form)
    if form.validate():
        form.save()
        flash(u"该生成功选择该课程!")
        return render_template('teacher/add_stu.html')
    for fieldName, errorMessages in form.errors.iteritems():
        for err in errorMessages:
            flash(err)
    return render_template('teacher/add_stu.html')