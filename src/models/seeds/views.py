from flask import Blueprint, request, render_template, url_for, session, redirect
from src.models.seeds.seed import Seed
from src.models.users.user import User
from werkzeug.utils import secure_filename
import os
from src import app


seed_blueprint = Blueprint('seeds', __name__)


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@seed_blueprint.route('/add', methods=['POST', 'GET'])
def add_seed():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        file = request.files['image']
        user = User.find_by_username(session['username'])
        user_id = user._id

        newpath = 'static/uploads/' + session['username']
        if not os.path.exists(newpath):
            os.makedirs(newpath)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            file.save(os.path.join(newpath, filename))
            if request.form.get('private'):
                _private = "private"
            else:
                _private = "public"
            seed = Seed(title=title, content=content, private=_private, image=filename, user_id=user_id)
            seed.save_to_mongo()
            return redirect(url_for('.view_seeds'))
    return render_template('/seeds/add_seed.html')

@seed_blueprint.route('/view')
def view_seeds():
    user = User.find_by_username(session['username'])
    user_id = user._id
    seeds = Seed.find_by_user(user_id)
    return render_template('/seeds/view_seeds.html', seeds=seeds)

@seed_blueprint.route('/view/<string:seed_id>')
def view_seeds_detail(seed_id):
    seed = Seed.find_by_id(seed_id)
    return render_template('/seeds/seed_detail.html', seed=seed)

@seed_blueprint.route('/view/<string:seed_id>/delete')
def delete_seed(seed_id):
    Seed.delete(seed_id)
    return redirect(url_for('.view_seeds'))

@seed_blueprint.route('/update/<string:seed_id>', methods=['POST', 'GET'])
def update_seed(seed_id):
    pass