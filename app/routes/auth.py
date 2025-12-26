from flask import Blueprint, render_template, request, flash, redirect, url_for
from ..models import db, Music, User
from ..logs import new_log
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    new_log("Пользователь зашел на страницу /signup")
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            flash('This username is already taken.')
            return redirect(url_for('signup'))

        new_user = User(
            username=username, 
            password=generate_password_hash(password, method='pbkdf2:sha256')
        )
        db.session.add(new_user)
        db.session.commit()
        
        flash('Success! Please login.')
        return redirect(url_for('auth.login'))
        
    return render_template('signup.html')




@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    new_log("Пользователь зашел на страницу /login")
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.index'))
        
        flash('Invalid username or password')
    return render_template('login.html')



@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))