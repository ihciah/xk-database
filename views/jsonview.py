#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from flask import Blueprint
from flask import g, request, flash
from flask import render_template, redirect, url_for,current_app
from utils import login_user,require_stu,gen_course_table,get_credit
from forms import DotkForm,DoxkFrom

__all__ = ['bp']

bp = Blueprint('jsonview',__name__)
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

@bp.route('/credit',methods=['GET'])
@require_stu
def credit():
    result={}
    result['credit']=get_credit(g.user.username)
    return json.dumps(result)