from flask import Blueprint, render_template, url_for, session, request, redirect, jsonify
from src.models.users.user import User
import src.models.users.errors as UserError
from src.common.utils import Utils
import os
from werkzeug.utils import secure_filename
from src.models.seeds.seed import Seed
import datetime
from datetime import timedelta



user_blueprint = Blueprint('users', __name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@user_blueprint.route('/register', methods=['POST', 'GET'])
def user_register():
    if request.method == 'POST':
        username = request.form['username']
        username = username.lower()
        password = request.form['password']
        re_password = request.form['re-password']
        email = request.form['email']
        file = request.files['image']
        filename = ""


        if password == re_password:


            newpath = 'static/uploads'
            if not os.path.exists(newpath):
                os.makedirs(newpath)

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)

                file.save(os.path.join(newpath, filename))
            if User.register_user(username, password, email, filename):
                session['username'] = username
                return redirect(url_for('.index'))
        else:
            raise UserError.RetypePassword("Please confirm the two fields of password are the same")
    return render_template('/users/register.html')

@user_blueprint.route('/logout')
def user_logout():
    session['username'] = None
    return redirect(url_for('home'))

@user_blueprint.route('/login', methods=['POST', 'GET'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.is_valid_login(username, password):
            session['username'] = username
            return redirect(url_for('.index'))

    return render_template('/users/login.html')



@user_blueprint.route('/reset-password/<string:username>', methods=['POST', 'GET'])
def reset_password(username):
    user = User.find_by_username(username)
    if request.method == 'POST':
        origin = request.form['origin']
        new = request.form['new']
        re_password = request.form['re_password']

        if Utils.check_hashed_password(origin, user.password):
            if new == re_password:
                user.password = Utils.hash_password(new)
                user.save_to_mongo()
                return redirect(url_for('.index'))
            else:
                raise UserError.RetypePassword("Your new password and re-type password are not the same")
        else:
            raise UserError.PasswordIncorrect("Your origin password is not correct")

    return render_template('/users/reset_password.html')



@user_blueprint.route('/setting/<string:username>', methods=['POST', 'GET'])
def update_user(username):
    user = User.find_by_username(username)
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        file = request.files['image']
        filename = ""


        newpath = 'static/uploads'
        if not os.path.exists(newpath):
            os.makedirs(newpath)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            file.save(os.path.join(newpath, filename))

        user.username = username
        user.email = email
        if filename:
            user.image = filename
        user.save_to_mongo()
        session['username']=username
        return redirect(url_for('.index'))
    return render_template('/users/update_user.html', user=user)



@user_blueprint.route('/search_friends', methods=['POST', 'GET'])
def search_friends_result():
    results = []
    user = User.find_by_username(session['username'])
    if request.method == 'POST':
        search_term = request.form['search']
        search_term = search_term.lower()
        if search_term != '':
            results = User.search_friend(search_term)

    return render_template('/users/search_friends.html', results=results, user=user)

@user_blueprint.route('/add_friend/<string:username>')
def add_friend(username):
    user = User.find_by_username(session['username'])
    user.add_friends(username)
    return redirect(url_for('.view_friends'))


@user_blueprint.route('/view_friends')
def view_friends():
    results = []
    friends = User.view_friends(session['username'])
    for friends in friends:
        results.append(User.find_by_username(friends.friend))
    return render_template('/users/view_friends.html', results=results)

@user_blueprint.route('/view_friends/<string:user_id>')
def friends_detail(user_id):
    user = User.find_by_id(user_id)
    seeds = user.find_seeds_by_user()
    return render_template('/users/users_detail.html', seeds=seeds, user=user)

@user_blueprint.route('/delete/<string:username>')
def delete_friend(username):
    friend = User.find_by_username(username)
    friend.delete(username)
    user = User.find_by_username(session['username'])
    user.friends.remove(username)
    user.save_to_mongo()

    return redirect(url_for('.view_friends'))

@user_blueprint.route('/')
def index():
    friends = User.view_friends(session['username'])
    if friends:
        for friends in friends:
            user = User.find_by_username(friends.friend)
            seeds = Seed.find_by_user(user._id)

            return render_template('/users/show_activities.html', seeds=seeds, user=user, standard=datetime.timedelta(0))
    return render_template('/users/no_activities.html')

