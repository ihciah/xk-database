#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import g, request, flash
from flask import render_template, redirect, url_for,current_app
from utils import login_user,require_stu,gen_course_table
from models import Student
from forms import ProfileForm

from models import Account
__all__ = ['bp']

bp = Blueprint('stu',__name__)
@bp.route('/',methods=['GET'])
@require_stu
def home():
    tt=gen_course_table(g.user.username)
    current_app.logger.debug(tt)
    return render_template('student/table.html',username=g.user.username,timetable=tt)

@bp.route('/profile',methods=['GET','POST'])
@require_stu
def profile():
    user = Student.query.get(g.user.username)
    if request.method == 'GET':
        return render_template('student/profile.html',username=g.user.username,name=user.name,age=user.age,major=user.major,grade=user.grade)
    form = ProfileForm(request.form)
    if form.validate():
        form.save()
        flash(u"资料成功更新!")
        user = Student.query.get(g.user.username)
        render_template('student/profile.html',username=g.user.username,name=user.name,age=user.age,major=user.major,grade=user.grade)
    for fieldName, errorMessages in form.errors.iteritems():
        for err in errorMessages:
            flash(err)
    return render_template('student/profile.html',username=g.user.username,name=user.name,age=user.age,major=user.major,grade=user.grade)