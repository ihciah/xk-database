#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import g, request, flash
from flask import render_template, redirect, url_for,current_app
from utils import login_user,require_stu,gen_course_table,get_credit
from models import Student
from forms import ProfileForm,SearchForm

from models import Account
__all__ = ['bp']

bp = Blueprint('stu',__name__)
@bp.route('/',methods=['GET'])
@require_stu
def home():
    tt=gen_course_table(g.user.username)
    return render_template('student/table.html',username=g.user.username,timetable=tt)

@bp.route('/profile',methods=['GET','POST'])
@require_stu
def profile():
    user = Student.query.get(g.user.username)
    if request.method == 'GET':
        return render_template('student/profile.html',name=user.name,age=user.age,major=user.major,grade=user.grade)
    form = ProfileForm(request.form)
    if form.validate():
        form.save()
        flash(u"资料成功更新!")
        user = Student.query.get(g.user.username)
        render_template('student/profile.html',name=user.name,age=user.age,major=user.major,grade=user.grade)
    for fieldName, errorMessages in form.errors.iteritems():
        for err in errorMessages:
            flash(err)
    return render_template('student/profile.html',name=user.name,age=user.age,major=user.major,grade=user.grade)

@bp.route('/xk',methods=['GET','POST'])
@require_stu
def xk():
    #stu_credit=get_credit(g.user.username)
    #g.user.credit=stu_credit
    if request.method == 'GET':
        return render_template('student/xk.html')
    form=SearchForm(request.form)
    if form.validate():
        sres=form.search()
        return render_template('student/xk.html',result=sres)
    #for fieldName, errorMessages in form.errors.iteritems():
    #    for err in errorMessages:
    #        flash(err)
    return render_template('student/xk.html')