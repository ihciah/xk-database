#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import g, request, flash
from flask import render_template, redirect, url_for,current_app
from utils import login_user,require_stu,gen_course_table

from models import Account
__all__ = ['bp']

bp = Blueprint('stu',__name__)
@bp.route('/',methods=['GET'])
@require_stu
def home():
    tt=gen_course_table(g.user.username)
    current_app.logger.debug(tt)
    return render_template('student/table.html',username=g.user.username,timetable=tt)