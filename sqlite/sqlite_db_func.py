import sqlite3

from flask import current_app, g

from .sqlite_db import get_db

def user_signup(username, hashed_password):
    db = get_db()
    error = None
    try:
        db.execute(
            "INSERT INTO user (username, password) VALUES (?, ?)",
            (username, hashed_password),
        )
        db.commit()
    except db.IntegrityError:
        error = f"User {username} is already registered."
    
    return error

def get_user_by_name(username):
    db = get_db()
    user = db.execute(
        'SELECT * FROM user WHERE username = ?', (username,)
    ).fetchone()
    return user


def get_user_by_id(user_id):
    db = get_db()
    user = db.execute(
        'SELECT * FROM user WHERE id = ?', (user_id,)
    ).fetchone()
    return user
