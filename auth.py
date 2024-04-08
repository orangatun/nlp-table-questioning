import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from .sqlite.sqlite_db_func import user_signup, get_user_by_name, get_user_by_id
# from .mysql.mysql_db_func import user_signup, get_user_by_name, get_user_by_id

messgs = []
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup', methods=('GET', 'POST'))
def signup():
    """Returns a view
    When the user submits a signup form in a POST req, the user is added to db and redirects to Login view.
    If the user is already logged in, it returns an "already signed in" view, and a "signup" view otherwise.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            error = user_signup(username=username, hashed_password=generate_password_hash(password))
            if not error:
                return redirect(url_for("auth.login"))

        flash(error)
    elif session:
        return render_template('auth/signedin.html')
        
    return render_template('auth/signup.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    """Returns a view
    Verifies the user login information against data in the database.
    On successful login, it redirects to user home page.
    On failure, it returns a login view.
    If the user is already logged in, it returns an "already signed in" view.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = get_user_by_name(username)
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            messgs.clear()
            return redirect(url_for('home.home'))

        flash(error)
    elif session:
        return render_template('auth/signedin.html')


    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    """Runs before each request
    Checks if there's a user already logged in.
    If a user is logged in, the user_id must be in the sessino.
    """
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_user_by_id(user_id)

@bp.route('/logout')
def logout():
    """Redirects to generic home view after logout
    Clears session data and redirects to home view.
    """
    session.clear()
    return redirect(url_for('home.home'))

def login_required(view):
    """Redirects the user to login page for pages accessed when not logged in.
    It wraps a view with a check for login. 
    For example, a user history view requires user to be logged in. 
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view