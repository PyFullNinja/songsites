import os
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models import db, User
from models import *
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-key-123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Маршруты (Routes) ---

@app.route('/')
def index():
    all_songs = Music.query.all()

    return render_template('index.html', all_songs=all_songs)

@app.route('/beats')
def beats():
    all_songs = Music.query.all()

    return render_template('beats.html', all_songs=all_songs)

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
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
        return redirect(url_for('login'))
        
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))



# Настройки папок для загрузки (можно вынести в config)
UPLOAD_FOLDER_MUSIC = 'static/uploads/music'
UPLOAD_FOLDER_AVATARS = 'static/uploads/avatars'
os.makedirs(UPLOAD_FOLDER_MUSIC, exist_ok=True)
os.makedirs(UPLOAD_FOLDER_AVATARS, exist_ok=True)

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if not current_user.is_admin:
        return 

    if request.method == 'POST':
        # 1. Получаем текстовые данные
        title = request.form.get('title')
        genre = request.form.get('genre')
        bpm = request.form.get('bpm')
        key = request.form.get('key')
        description = request.form.get('description')
        
        # Получаем цены и конвертируем в float (если не пусто)
        p_mp3 = request.form.get('price_mp3')
        p_wav = request.form.get('price_wav')
        p_trackout = request.form.get('price_track_out')
        p_exclusive = request.form.get('price_exclusive')

        # 2. Обработка файлов
        music_file = request.files.get('music_file')
        avatar_file = request.files.get('avatar_file')

        if music_file and music_file.filename != '':
            music_filename = secure_filename(music_file.filename)
            music_path = os.path.join(UPLOAD_FOLDER_MUSIC, music_filename)
            music_file.save(music_path)
        else:
            flash("Файл музыки обязателен!")
            return redirect(request.url)

        avatar_path = None
        if avatar_file and avatar_file.filename != '':
            avatar_filename = secure_filename(avatar_file.filename)
            avatar_path = os.path.join(UPLOAD_FOLDER_AVATARS, avatar_filename)
            avatar_file.save(avatar_path)

        # 3. Сохранение в базу данных
        new_music = Music(
            title=title,
            file_path=music_path, # Сохраняем путь к файлу
            avatar_path=avatar_path,
            genre=genre,
            bpm=int(bpm) if bpm else None,
            key=key,
            description=description,
            price_mp3=float(p_mp3) if p_mp3 else None,
            price_wav=float(p_wav) if p_wav else None,
            price_track_out=float(p_trackout) if p_trackout else None,
            price_exclusive=float(p_exclusive) if p_exclusive else None
        )

        try:
            db.session.add(new_music)
            db.session.commit()
            flash("Трек успешно загружен!")
            return redirect(url_for('index')) # Или на главную
        except Exception as e:
            db.session.rollback()
            flash(f"Ошибка при сохранении в базу: {e}")

    return render_template('upload.html')



@app.route('/order')
def order():
    return render_template('order.html')


@app.route('/buy/<int:song_id>')
def buy(song_id):
    song = Music.query.get_or_404(song_id)
    return render_template('shop.html', song=song)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)