#!/usr/bin/env python
# coding: utf-8
import os,sys
from flask_script import Manager, Server
from flask.ext.migrate import Migrate, MigrateCommand
from app import create_app
from models import db

sys.path.append(os.path.abspath(''))
app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
