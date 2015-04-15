from flask import Blueprint
from flask import render_template
__all__ = ['bp']

bp = Blueprint('account',__name__)
@bp.route('/signup',methods=['GET', 'POST'])
def signup():
    return render_template('account/signup.html')