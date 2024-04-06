import os
import functools
import csv

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
from werkzeug.utils import secure_filename

from .auth import messgs

from .ai_model import query

from .sqlite.sqlite_db_func import add_file, get_user_by_name, add_question, add_response_to_question

bp = Blueprint('home', __name__, url_prefix='/')

UPLOAD_FOLDER = os.path.abspath('../uploads')
ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/', methods = ('GET', 'POST'))
def home():
    if session:
        return render_template('home/user-home.html')
    else:
        return render_template('home/general-home.html')

@bp.route('/upload', methods = ('GET', 'POST'))
def file_upload():
    if session:
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                session['filename'] = filename
                session['filepath'] = os.path.join(current_app.instance_path+"/uploads", filename)
                session['file_id'] = None
                file.save(os.path.join(current_app.instance_path+"/uploads", filename))
                (error, inserted_id) = add_file(get_user_by_name(username=session['username'])['id'],filename, file_path=session['filepath'])
                if error is not None:
                    flash(error)
                else:
                    flash(f"file saved to database with id {inserted_id}")
                    session['file_id'] = inserted_id
                data = {}
                with open(session['filepath'], newline='') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        for key, value in row.items():
                            data[key] = data.get(key, []) + [value]
                session['filedata'] = data
                flash("File uploaded successfully")

            else:
                flash('Invalid file extension')
                # return redirect(url_for('download_file', name=filename))
        return render_template('home/user-home.html')
    else:
        return render_template('home/general-home.html')


@bp.route('/question', methods = ('GET', 'POST'))
def question():
    if session:
        if request.method == 'POST':
            # check if the file is in the session
            if session['file_id']:
                question = request.form['question']
                (error, inserted_id) = add_question(session['file_id'],question)
                if error is not None:
                    flash(error)
                elif inserted_id == "-1":
                    flash("Insertion of question in database failed.")
                else:
                    flash(question)
                    messgs.append(f"u{question}")
                    answer = query(question)
                    (error, updated_id) = add_response_to_question(answer, inserted_id)
                    if error is not None:
                        flash(error)
                    elif inserted_id == "-1":
                        flash(f"Updation of answer in database failed for question {inserted_id}")
                    else:
                        flash(answer)
                        messgs.append(f"a{answer}")
            else:
                flash('Question is not saved in database. Please try again')
        return render_template('home/user-home.html', messgs = messgs)
    else:
        return render_template('home/general-home.html')

