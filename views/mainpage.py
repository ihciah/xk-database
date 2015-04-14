#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, request, current_app
from flask import render_template, redirect, abort
from flask import url_for, jsonify
__all__ = ['bp']
bp = Blueprint('mainpage',__name__)

@bp.route('/')
def home():
    return render_template(
        'index.html',name="ihciah"
    )