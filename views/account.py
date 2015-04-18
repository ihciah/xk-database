#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import render_template
from flask import g, request, flash, current_app
from flask import render_template, redirect, url_for,current_app
from forms import SignupForm
from utils import login_user

from models import Account
__all__ = ['bp']

bp = Blueprint('account',__name__)
@bp.route('/signup',methods=['GET', 'POST'])
def signup():
    roles={1:"stu",2:"admin",3:"teacher"}
    if request.method == 'GET':
        return render_template('account/signup.html')
    form = SignupForm(request.form)
    if form.validate():
        usr=form.save()
        login_user(usr)
        return redirect("/stu")
    for fieldName, errorMessages in form.errors.iteritems():
        for err in errorMessages:
            flash(err)
    return render_template('account/signup.html')


@bp.route('/login',methods=['GET', 'POST'])
def login():
     if request.method == 'GET':
        flash(u'测试消息:密码错误!')
        return render_template('account/login.html')


