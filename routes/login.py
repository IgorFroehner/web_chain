from hashlib import sha256

from flask import render_template, redirect
from flask_login import login_user, login_required, logout_user
from flask import Blueprint

from model import LoginForm
from model import user_dao

from routes import blockchain

from app import login_manager

blue = Blueprint('login', __name__, static_folder='static', template_folder='templates')


@login_manager.user_loader
def user_loader(user):
    return user_dao.find_by_user(user)


@login_manager.unauthorized_handler
def unauthorized():
    return render_template('unauthorized.html')


@blue.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')


@blue.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = user_dao.find_by_user(form.user.data)
        if user is not None:
            if user.password == sha256(form.password.data.encode('utf-8')).hexdigest():
                login_user(user)
                return redirect('/')
        else:
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)
