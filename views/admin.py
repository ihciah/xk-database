#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import g, request, flash, current_app
from flask import render_template, redirect, url_for,current_app
from models import Student,Account,Course,Xk
from sqlalchemy.sql import func
from forms import SearchStudentFrom,adminProfileForm
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
        result=form.dosearch()
        return render_template('admin/user_search_result.html',result=result)
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
