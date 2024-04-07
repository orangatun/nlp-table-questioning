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
    inserted_id = None
    try:
        inserted_id = db.execute(
            "INSERT INTO csv_file (user_id, file_name, file_path) VALUES (?, ?, ?) RETURNING id",
            (user_id, file_name, file_path),
        ).fetchone()['id']
        db.commit()
    except db.IntegrityError:
        error = f"File insertion failed."
    
    if inserted_id is not None and error is None:
        return (error, inserted_id)
    return (error, "-1")

def get_file_id_by_name(user_id, file_name):
    db = get_db()
    # If there are multiple uploads by the same user, with a file with the same name
    # this returns the id of most recent file uploaded by a user with a file name
    file_id = db.execute(
        'SELECT id FROM csv_file WHERE user_id = ? AND file_name = ? ORDERBY uploaded DESC', (user_id, file_name)
    ).fetchone()

    return file_id


def add_question(file_id, question):
    db = get_db()
    error = None
    inserted_id = None
    try:
        inserted_id = db.execute(
            "INSERT INTO question (file_id, question) VALUES (?, ?) RETURNING id",
            (file_id, question),
        ).fetchone()['id']
        db.commit()
    except db.IntegrityError:
        error = f"Question insertion failed."
    
    if inserted_id is not None and error is None:
        return (error, inserted_id)
    return (error, "-1")

def add_response_to_question(answer, question_id):
    db = get_db()
    error = None
    try:
        updated_id = db.execute(
            "UPDATE question SET response = ? WHERE id = ? RETURNING id", 
            (answer, question_id),
        ).fetchone()['id']
        db.commit()
    except db.Error:
        error = "Updating answer failed."

    if updated_id is not None and error is None:
        return (error, updated_id)
    return (error, "-1")

def get_questions_by_user_id(user_id):
    db = get_db()
    files = db.execute(
        'SELECT f.id as file_id, f.file_name as file_name, f.uploaded as uploaded, q.id as question_id, q.req_time as question_time, q.question as question, q.response as response FROM user u JOIN csv_file f ON u.id = f.user_id LEFT JOIN question q ON f.id = q.file_id WHERE u.id = ? ORDER BY u.id, f.id, q.id', (user_id,)
    ).fetchall()
    return files
