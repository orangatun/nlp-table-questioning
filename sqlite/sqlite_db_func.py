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

def add_file(user_id, file_name, file_path):
    db = get_db()
    error = None
    try:
        db.execute(
            "INSERT INTO file (user_id, file_name, file_path) VALUES (?, ?, ?)",
            (user_id, file_name, file_path),
        )
        db.commit()
    except db.IntegrityError:
        error = f"File insertion failed."
    
    return error

def get_file_id_by_name(user_id, file_name):
    db = get_db()
    # If there are multiple uploads by the same user, with a file with the same name
    # this returns the id of most recent file uploaded by a user with a file name
    file_id = db.execute(
        'SELECT id FROM file WHERE user_id = ? AND file_name = ? ORDERBY uploaded DESC', (user_id, file_name)
    ).fetchone()

    return file_id

