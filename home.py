import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('home', __name__, url_prefix='/')

@bp.route('/')
def home():
    if session:
        return render_template('home/user-home.html')
    else:
        return render_template('home/general-home.html')
