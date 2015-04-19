#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import render_template
from flask import g, request, flash, current_app
from flask import render_template, redirect, url_for,current_app
from forms import SignupForm
from utils import get_current_user,require_admin

from models import Account
__all__ = ['bp']

bp = Blueprint('admin',__name__)
@bp.route('/',methods=['GET'])
@require_admin
def home():
    return render_template('admin/admin.html',username=g.user.username)
