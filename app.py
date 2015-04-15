#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask

def create_app():
    app = Flask(__name__,template_folder='templates')
    app.config.from_pyfile('_settings.py')
    register_routes(app)
    return app

def register_routes(app):
    from views import mainpage,account
    app.register_blueprint(account.bp, url_prefix='/account')
    app.register_blueprint(mainpage.bp, url_prefix='/')
