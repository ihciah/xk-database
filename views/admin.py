#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import g, request, flash
from flask import render_template, redirect
from models import Student,Account,Course,Xk,Teacher
from forms import SearchStudentFrom,adminProfileForm,UserProfileForm,SearchForm,CourseEditForm,UseraddForm
from utils import get_current_user,require_admin,transt2line,transtea2line

__all__ = ['bp']

bp = Blueprint('admin',__name__)
@bp.route('/',methods=['GET'])
@require_admin
def home():
    user_count=Account.query.filter(Account.role!=2).count()
    course_count=Course.query.count()
    return render_template('admin/admin.html',user_count=user_count,course_count=course_count)

@bp.route('/userlist',methods=['GET','POST'])
@require_admin
def userlist():
    if request.method == 'GET':
        return render_template('admin/user_search.html')
    form = SearchStudentFrom(request.form)
    if form.validate():
        [result_student,result_teacher]=form.dosearch()
        return render_template('admin/user_search_result.html',result_student=result_student,result_teacher=result_teacher)
    for fieldName, errorMessages in form.errors.iteritems():
        for err in errorMessages:
            flash(err)
    return render_template('admin/user_search.html')

@bp.route('/profile',methods=['GET','POST'])
@require_admin
def profile():
    user = Student.query.get(g.user.username)
    if request.method == 'GET':
        return render_template('admin/profile.html')
    form = adminProfileForm(request.form)
    if form.validate():
        form.save()
        flash(u"资料成功更新!")
        user = Student.query.get(g.user.username)
        render_template('admin/profile.html')
    for fieldName, errorMessages in form.errors.iteritems():
        for err in errorMessages:
            flash(err)
    return render_template('admin/profile.html')

@bp.route('/stu-course',methods=['GET'])
@require_admin
def stu_course():
    #查看学生选课、选课退课
    uid=request.args.get('id')
    if uid is None or uid=='':
        return redirect("/admin/userlist")
    return render_template('admin/stu_course.html',result=Student.query.get(uid),uid=uid)


@bp.route('/user-profile',methods=['GET','POST'])
@require_admin
def user_profile():
    #修改教师/学生资料
    if request.method == 'GET':
        uid=request.args.get('id')
        if uid is None:
            return redirect("/admin/userlist")
        user=Student.query.get(uid)
        if user is None:
            user=Teacher.query.get(uid)
            if user is None:
                return redirect("/admin/userlist")
            return render_template('admin/user_profile.html',stu=None,tea=user)
        return render_template('admin/user_profile.html',stu=user,tea=None)

    form=UserProfileForm(request.form)

    if form.validate():
        form.save()
        flash(u"资料成功更新!")
    #current_app.logger.debug(3)
    for fieldName, errorMessages in form.errors.iteritems():
        for err in errorMessages:
            flash(err)
    #current_app.logger.debug(2)
    if form.stuid is not None and form.stuid.data!='':
        user=Student.query.get(form.stuid.data)
        return render_template('admin/user_profile.html',stu=user,tea=None)
    else:
        user=Teacher.query.get(form.teaid.data)
        return render_template('admin/user_profile.html',stu=None,tea=user)

@bp.route('/course',methods=['GET','POST'])
@require_admin
def course():
    if request.method == 'GET':
        return render_template('admin/courselist.html')
    form = SearchForm(request.form)
    if form.validate():
        sres=form.search()
        return render_template('admin/courselist.html',result=sres)
    return render_template('admin/courselist.html')

@bp.route('/course-edit',methods=['GET','POST'])
@require_admin
def course_edit():
    if request.method == 'GET':
        code=request.args.get('id')
        if code is None or code=='':
            course=None
            times=None
            teas=None
            type=1#1:new;0:edit
        else:
            type=0
            course=Course.query.get(code)
            if course is None:
                return redirect("/admin/course")
            times=transt2line(course.ctime)
            teas=transtea2line(course.teacher)
        return render_template('admin/course_edit.html',type=type,course=course,times=times,teas=teas)
    form = CourseEditForm(request.form)
    course=times=teas=None
    if form.validate():
        course=form.save()
        flash(u"课程保存成功!")
    else:
        course=Course.query.get(form.code.data)
    times=transt2line(course.ctime)
    teas=transtea2line(course.teacher)
    for fieldName, errorMessages in form.errors.iteritems():
        for err in errorMessages:
            flash(err)
    return render_template('admin/course_edit.html',type=0,course=course,times=times,teas=teas)

@bp.route('/useradd',methods=['GET', 'POST'])
@require_admin
def signup():
    roles={1:"stu",2:"admin",3:"teacher"}
    if request.method == 'GET':
        return render_template('admin/useradd.html')
    form = UseraddForm(request.form)
    if form.validate():
        uid,type=form.save()
        flash(u"用户添加成功!")
        if type==1 or type==3:
            return redirect("/admin/user-profile?id="+uid)
        return redirect("/admin/useradd")
    for fieldName, errorMessages in form.errors.iteritems():
        for err in errorMessages:
            flash(err)
    return render_template('admin/useradd.html')

@bp.route('/course-stu',methods=['GET'])
@require_admin
def course_stu():
    cid=request.args.get('id')
    if cid is None or cid=='':
        return redirect("/admin/course")
    result_student=Student.query.join(Xk, Xk.stuid==Student.stuid).filter(Xk.code==cid).all()
    return render_template('admin/course_user.html',result_student=result_student,result_teacher=None,courseid=cid)