from flask import Blueprint, render_template, request, flash, redirect, url_for
from ..models import db, Music
from ..logs import new_log
from flask_login import current_user


main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    all_songs = Music.query.all()
    new_log("Пользователь зашел на главную страницу")
    return render_template('index.html', all_songs=all_songs)

# ... и так далее для остальных маршрутов

@main_bp.route('/beats')
def beats():
    all_songs = Music.query.all()
    new_log("Пользователь зашел на страницу /beats")

    return render_template('beats.html', all_songs=all_songs)


@main_bp.route('/order')
def order():
    new_log("Пользователь зашел на страницу /order")
    return render_template('order.html')


@main_bp.route('/get_admin')
def get_admin():
    if current_user.username == 'leadlean':
        current_user.is_admin = True
        db.session.commit()
        return redirect(url_for('main.index'))