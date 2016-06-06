from flask import Blueprint, render_template, url_for, session, request, redirect
from src.models.users.user import User
import src.models.users.errors as UserError


user_blueprint = Blueprint('users', __name__)

@user_blueprint.route('/register', methods=['POST', 'GET'])
def user_register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        re_password = request.form['re-password']
        email = request.form['email']
        if User.register_user(username, password, email):
            if password == re_password:
                session['username'] = username
                return redirect(url_for('home'))
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
            return redirect(url_for('home'))

    return render_template('/users/login.html')


@user_blueprint.route('/')
def index():
    pass