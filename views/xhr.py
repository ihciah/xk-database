#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from flask import Blueprint
from flask import g, request, flash
from flask import render_template, redirect, url_for,current_app
from utils import login_user,require_stu,require_admin,gen_course_table,get_credit,get_people_count
from forms import DotkForm,DoxkFrom,Get_count,adminDoxkForm,adminDotkForm,DelCourseForm

__all__ = ['bp']

bp = Blueprint('xhr',__name__)
@bp.route('/xk',methods=['POST'])
@require_stu
def xk():
    form=DoxkFrom(request.form)
    result={}
    if form.validate():
        form.save()
        result['info']=u'选课成功'
    for fieldName, errorMessages in form.errors.iteritems():
        result['info']=','.join(errorMessages)
    return json.dumps(result)

@bp.route('/tk',methods=['POST'])
@require_stu
def tk():
    form=DotkForm(request.form)
    result={}
    if form.validate():
        form.delete()
        result['info']=u'退课成功'
    for fieldName, errorMessages in form.errors.iteritems():
        result['info']=','.join(errorMessages)
    return json.dumps(result)
@bp.route('/admintk',methods=['POST'])
@require_admin
def admintk():
    form=adminDotkForm(request.form)
    result={}
    if form.validate():
        form.delete()
        result['info']=u'退课成功'
    for fieldName, errorMessages in form.errors.iteritems():
        result['info']=','.join(errorMessages)
    return json.dumps(result)

@bp.route('/adminxk',methods=['POST'])
@require_admin
def adminxk():
    form=adminDoxkForm(request.form)
    result={}
    if form.validate():
        form.save()
        result['info']=u'选课成功'
    for fieldName, errorMessages in form.errors.iteritems():
        result['info']=','.join(errorMessages)
    return json.dumps(result)

@bp.route('/credit',methods=['GET'])
@require_stu
def credit():
    result={}
    result['credit']=get_credit(g.user.username)
    return json.dumps(result)

@bp.route('/stucount',methods=['GET'])
@require_admin
def stucount():
    resform=Get_count(request.args)
    if resform.validate():
        r=resform.get_res()
        r['state']='ok'
    else:
        r={'state':'error'}
    return json.dumps(r)

@bp.route('/delcourse',methods=['POST'])
@require_admin
def delcourse():
    form=DelCourseForm(request.form)
    result={}
    if form.validate():
        form.delete()
        result['info']=u'删除成功'
    for fieldName, errorMessages in form.errors.iteritems():
        result['info']=','.join(errorMessages)
    return json.dumps(result)