#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import render_template
from flask import g, request, flash, current_app
from flask import render_template, redirect, url_for,current_app
from forms import SignupForm,LoginForm
from utils import login_user,get_current_user,logout_user

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
     roles={1:"stu",2:"admin",3:"teacher"}
     if request.method == 'GET':
         usr = get_current_user()
         if usr is not None:
             return redirect("/"+roles[usr.role])
         return render_template('account/login.html')
     form = LoginForm(request.form)
     if form.validate():
         login_user(form.user)
         return redirect("/"+roles[form.user.role])
     for fieldName, errorMessages in form.errors.iteritems():
        for err in errorMessages:
            flash(err)
     return render_template('account/login.html')

@bp.route('/logout',methods=['GET'])
def logout():
    logout_user()
    flash(u"已登出您的账号")
    return render_template('account/login.html')