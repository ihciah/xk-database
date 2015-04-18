import sys
from flask import g, request, session, current_app
from flask import url_for, redirect, abort, flash
sys.path.append("D:/CODE/xk-database")
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
            if not g.user:
                url = url_for('account.signin')
                if '?' not in url:
                    url += '?next=' + request.url
                return redirect(url)
            if self.roles[self.role]!=self.roles[g.user.role]:
                return abort(403)
            return method(*args, **kwargs)
        return wrapper

require_stu = require_role('student')
require_admin = require_role('admin')
require_teacher = require_role('teacher')

def login_user(user, permanent=False):
    if not user:
        return None
    session['id'] = user.id
    if permanent:
        session.permanent = True
    return user


def logout_user():
    if 'id' not in session:
        return
    session.pop('id')


def get_current_user():
    if 'id' in session:
        user = Account.query.get(int(session['id']))
        if not user:
            return None
        return user
    return None
