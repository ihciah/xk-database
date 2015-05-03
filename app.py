#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,os
sys.path.append(os.path.abspath(''))
from flask import Flask
from models import db

def create_app():
    app = Flask(__name__,template_folder='templates')
    app.config.from_pyfile('_settings.py')
    register_routes(app)
    register_database(app)
    return app

def register_routes(app):
    from views import mainpage,account,admin,stu,teacher,xhr
    app.register_blueprint(mainpage.bp, url_prefix='/')
    app.register_blueprint(account.bp, url_prefix='/account')
    app.register_blueprint(xhr.bp, url_prefix='/xhr')
    app.register_blueprint(admin.bp, url_prefix='/admin')
    app.register_blueprint(stu.bp, url_prefix='/stu')
    app.register_blueprint(teacher.bp, url_prefix='/teacher')

def register_database(app):
    db.init_app(app)
    db.app = app