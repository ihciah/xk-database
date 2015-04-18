from flask import Blueprint
from flask import render_template
from flask import g, request, flash, current_app
from flask import render_template, redirect, url_for
from models import Account
__all__ = ['bp']

bp = Blueprint('account',__name__)
@bp.route('/signup',methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('account/signup.html')

@bp.route('/login',methods=['GET', 'POST'])
def login():
     if request.method == 'GET':
        return render_template('account/login.html')

