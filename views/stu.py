#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import render_template
from flask import g, request, flash, current_app
from flask import render_template, redirect, url_for,current_app
from forms import SignupForm
from utils import login_user,require_stu

from models import Account
__all__ = ['bp']

bp = Blueprint('stu',__name__)
@bp.route('/',methods=['GET'])
@require_stu
def home():
    pass