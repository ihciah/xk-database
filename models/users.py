#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _base import db,SessionMixin
from werkzeug import security

__all__ = ['Account']
class Account(db.Model, SessionMixin):
    __tablename__ = "users"
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_general_ci'
    }
    username = db.Column(db.String(100), primary_key=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Integer,nullable=False)
    email = db.Column(db.String(100))

    def __init__(self, **kwargs):
        if 'password' in kwargs:
            raw = kwargs.pop('password')
            self.password = self.create_password(raw)

        if 'username' in kwargs:
            self.username = kwargs.pop('username')

        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def is_admin(self):
        return self.role==2
    @property
    def is_stu(self):
        return self.role==1
    @property
    def is_teacher(self):
        return self.role==3

    @staticmethod
    def create_password(raw):
        passwd = '{old}{new}'.format(old=raw, new=db.app.config['PASSWORD_SECRET'])
        return security.generate_password_hash(passwd)

    def change_password(self, raw):
        self.passwd = self.create_password(raw)
        return self

    def check_password(self, raw):
        passwd = '{old}{new}'.format(old=raw, new=db.app.config['PASSWORD_SECRET'])
        return security.check_password_hash(self.password, passwd)