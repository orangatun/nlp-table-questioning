import os
import functools
import csv

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
from werkzeug.utils import secure_filename

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
                data = []
                session['filepath'] = os.path.join(current_app.instance_path+"/uploads", filename)
                file.save(os.path.join(current_app.instance_path+"/uploads", filename))
                with open(session['filepath']) as file:
                    csv_file = csv.reader(file)
                    for row in csv_file:
                        data.append(row)
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
            if session['filedata']:
                question = request.form['question']
                flash(question)
            else:
                flash('No file data to ask questions')
        return render_template('home/user-home.html')
    else:
        return render_template('home/general-home.html')

