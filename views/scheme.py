#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import g, request, flash
from flask import render_template, redirect, url_for,current_app
from utils import login_user,require_stu,gen_course_table,get_credit
from models import Student
from forms import ProfileForm,SearchMajorCourse

from models import Account
__all__ = ['bp']

bp = Blueprint('scheme',__name__)
@bp.route('/',methods=['GET','POST'])
@require_stu
def xk():
    if request.method == 'GET':
        return render_template('scheme/recommend.html')
    form = SearchMajorCourse(request.form)
    #卧槽简直是坑啊，之前在这用wtform一切都没问题尼玛就是获取不到表单数据，索性SearchForm不继承Form，然后就过了，我勒个去，怀疑是wtform哪bug了
    if form.validate():
        sres=form.search()
        return render_template('scheme/recommend.html',result=sres)
    return render_template('scheme/recommend.html')