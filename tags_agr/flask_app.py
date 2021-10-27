import os
from os import environ
from threading import Thread

from flask import Flask, render_template, request, send_file
from flask_bootstrap import Bootstrap
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from tags_agr import UPLOAD_FOLDER_ADOBE, UPLOAD_FOLDER_RESIZE, UPLOAD_FOLDER_LONG
from tags_agr import db_tools, resize, long
from tags_agr.main import add_new_data

app = Flask(__name__)
auth = HTTPBasicAuth()
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'you-will-never-guess'
users = {
    environ.get('SITE_LOGIN') or 'root': generate_password_hash(environ.get('SITE_PASS') or 'pass'),
}


def upload(files, directory=UPLOAD_FOLDER_ADOBE):
    if not os.path.isdir(directory):
        os.mkdir(directory)
    for up_file in files:
        filename = secure_filename(up_file.filename)
        up_file.save(os.path.join(directory, filename))


@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username


@app.route('/', methods=['POST', 'GET'])
@auth.login_required
def index():
    search_results = []
    tag_stats = []
    if request.method == 'POST':
        files = request.files.getlist('file')
        title_for_search = request.form.get('title')
        tag_for_search = request.form.get('tag')
        if files:
            upload(files)
            tread = Thread(target=add_new_data)
            tread.start()
        elif title_for_search:
            search_results, tag_stats = db_tools.get_items_by_title(title_for_search.strip())
        elif tag_for_search:
            search_results, tag_stats = db_tools.get_items_by_tag(tag_for_search.strip())
    return render_template('index.html', search_results=search_results, tag_stats=tag_stats)


@app.route('/resize', methods=['POST', 'GET'])
@auth.login_required
def resize_img():
    status = {}
    if request.method == 'POST':
        tiny_files = request.files.getlist('tiny_file')
        long_files = request.files.getlist('long_file')
        resize_width = request.form.get('resize_width')
        if tiny_files:
            upload(tiny_files, UPLOAD_FOLDER_RESIZE)
            tread = Thread(target=resize.run, args=(resize_width,))
            tread.start()
        elif long_files:
            upload(long_files, UPLOAD_FOLDER_LONG)
            tread = Thread(target=long.run)
            tread.start()
    list_resize_upload_dir = os.listdir(UPLOAD_FOLDER_RESIZE)
    list_long_upload_dir = os.listdir(UPLOAD_FOLDER_LONG)
    if list_resize_upload_dir:
        status['tiny_progress'] = len(list_resize_upload_dir)
    elif os.path.exists('tiny_result.zip'):
        status['tiny_result'] = True

    if list_long_upload_dir:
        status['long_progress'] = len(list_long_upload_dir)
    elif os.path.exists('long_result.jpg'):
        status['long_result'] = True
    return render_template('resize.html', status=status)


@app.route("/last_tiny")
@auth.login_required
def last_tiny():
    if os.path.exists('tiny_result.zip'):
        return send_file(os.path.abspath('tiny_result.zip'))


@app.route("/last_long")
@auth.login_required
def last_long():
    if os.path.exists('long_result.jpg'):
        return send_file(os.path.abspath('long_result.jpg'))


if __name__ == "__main__":
    app.run(debug=True)
