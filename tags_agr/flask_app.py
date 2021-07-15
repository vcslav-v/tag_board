from os import environ
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash, generate_password_hash
from tags_agr.main import new_data
from tags_agr import db_tools

app = Flask(__name__)
auth = HTTPBasicAuth()
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'you-will-never-guess'
users = {
    environ.get('SITE_LOGIN') or 'root': generate_password_hash(environ.get('SITE_PASS') or 'pass'),
}


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
            new_data(files)
        elif title_for_search:
            search_results, tag_stats = db_tools.get_items_by_title(title_for_search.strip())
        elif tag_for_search:
            search_results, tag_stats = db_tools.get_items_by_tag(tag_for_search.strip())
    return render_template('index.html', search_results=search_results, tag_stats=tag_stats)


if __name__ == "__main__":
    app.run(debug=True)
