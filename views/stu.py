#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import g, request, flash
from flask import render_template, redirect, url_for,current_app
from utils import login_user,require_stu,gen_course_table,get_credit
from models import Student
from forms import ProfileForm,SearchForm,SearchMajorCourse,SearchMajorid

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
        return render_template('student/profile.html',user=user)
    form = ProfileForm(request.form)
    if form.validate():
        form.save()
        flash(u"资料成功更新!")
        user = Student.query.get(g.user.username)
        render_template('student/profile.html',user=user)
    for fieldName, errorMessages in form.errors.iteritems():
        for err in errorMessages:
            flash(err)
    return render_template('student/profile.html',user=user)

@bp.route('/xk',methods=['GET','POST'])
@require_stu
def xk():
    if request.method == 'GET':
        return render_template('student/xk.html')
    form = SearchForm(request.form)
    #卧槽简直是坑啊，之前在这用wtform一切都没问题尼玛就是获取不到表单数据，索性SearchForm不继承Form，然后就过了，我勒个去，怀疑是wtform哪bug了
    if form.validate():
        sres=form.search()
        return render_template('student/xk.html',result=sres)
    return render_template('student/xk.html')
    

@bp.route('/scheme/',methods=['GET','POST'])
@require_stu
def scheme():
    if request.method == 'GET':
        return render_template('scheme/recommend.html')
    form = SearchMajorCourse(request.form)
    #卧槽简直是坑啊，之前在这用wtform一切都没问题尼玛就是获取不到表单数据，索性SearchForm不继承Form，然后就过了，我勒个去，怀疑是wtform哪bug了
    if form.validate():
        sres=form.search()
        return render_template('scheme/recommend.html',result=sres)
    return render_template('scheme/recommend.html')


@bp.route('/suggestions/',methods=['GET','POST'])
@require_stu
def majorname():
    if request.method == 'GET':
        return render_template('scheme/majorid.html')
    form = SearchMajorid(request.form)
    #卧槽简直是坑啊，之前在这用wtform一切都没问题尼玛就是获取不到表单数据，索性SearchForm不继承Form，然后就过了，我勒个去，怀疑是wtform哪bug了
    if form.validate():
        sres=form.search()
        return render_template('scheme/majorid.html',result=sres)
    return render_template('scheme/majorid.html')

