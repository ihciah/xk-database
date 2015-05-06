#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import g, request, flash, current_app
from flask import render_template, redirect, url_for,current_app
from models import Student,Account,Course,Xk,Teacher
from sqlalchemy.sql import func
from forms import SearchStudentFrom,adminProfileForm,UserProfileForm
from utils import get_current_user,require_admin

__all__ = ['bp']

bp = Blueprint('admin',__name__)
@bp.route('/',methods=['GET'])
@require_admin
def home():
    user_count=Account.query.count()
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
    if request.method == 'GET':
        uid=request.args.get('id')
        if uid is None:
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
    current_app.logger.debug(3)
    for fieldName, errorMessages in form.errors.iteritems():
        for err in errorMessages:
            flash(err)
    current_app.logger.debug(2)
    if form.stuid is not None and form.stuid.data!='':
        user=Student.query.get(form.stuid.data)
        return render_template('admin/user_profile.html',stu=user,tea=None)
    else:
        user=Teacher.query.get(form.teaid.data)
        return render_template('admin/user_profile.html',stu=None,tea=user)