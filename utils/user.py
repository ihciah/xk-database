#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import g, request, session, current_app
from flask import url_for, redirect, abort, flash
import functools
from models import Account
class require_role(object):
    roles = {
        'student': 1,
        'admin': 2,
        'teacher': 3,
    }
    def __init__(self, role):
        self.role = role

    def __call__(self, method):
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            usr=get_current_user()
            if usr is not None and self.roles[self.role]==usr.role:
                g.user=usr
                return method(*args, **kwargs)
            return abort(403)
        return wrapper

require_stu = require_role('student')
require_admin = require_role('admin')
require_teacher = require_role('teacher')

def login_user(user, permanent=False):
    if not user:
        return None
    session['username'] = user.username
    session['role']=user.role
    if permanent:
        session.permanent = True
    return user


def logout_user():
    if 'username' not in session:
        return
    session.pop('username')


def get_current_user():
    if 'username' in session:
        user = Account.query.get(session['username'])
        if not user:
            return None
        return user
    return None
