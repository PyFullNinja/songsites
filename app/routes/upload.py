from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from ..models import db, Music
from ..logs import new_log
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from ..config import UPLOAD_FOLDER_MUSIC, UPLOAD_FOLDER_AVATARS

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/', methods=['GET', 'POST'])
@login_required
def upload():
    # Проверка прав администратора
    if not current_user.is_admin: 
        new_log("ВНИМАНИЕ! ПОЛЬЗОВАТЕЛЬ ПОПЫТАЛСЯ ЗАЙТИ НА СТРАНИЦУ /upload")
        abort(403)  # Возвращаем ошибку доступа

    if request.method == 'POST':
        try:
            # 1. Получаем текстовые данные
            title = request.form.get('title')
            genre = request.form.get('genre')
            bpm = request.form.get('bpm')
            key = request.form.get('key')
            description = request.form.get('description')
            
            # Получаем цены
            p_mp3 = request.form.get('price_mp3')
            p_wav = request.form.get('price_wav')
            p_trackout = request.form.get('price_track_out')
            p_exclusive = request.form.get('price_exclusive')

            # 2. Обработка основного файла MP3 (обязательный)
            music_file = request.files.get('music_file')
            if not music_file or music_file.filename == '':
                flash("Файл музыки (MP3) обязателен!")
                return redirect(request.url)
            
            music_filename = secure_filename(music_file.filename)
            music_path = os.path.join(UPLOAD_FOLDER_MUSIC, music_filename)
            music_file.save(music_path)

            # 3. Обработка опциональных файлов
            # WAV файл
            music_wav_path = None
            music_wav_file = request.files.get('music_wav_file')
            if music_wav_file and music_wav_file.filename != '':
                music_wav_filename = secure_filename(music_wav_file.filename)
                music_wav_path = os.path.join(UPLOAD_FOLDER_MUSIC, music_wav_filename)
                music_wav_file.save(music_wav_path)

            # Track Out файл
            track_out_path = None
            track_out_file = request.files.get('track_out_file')
            if track_out_file and track_out_file.filename != '':
                track_out_filename = secure_filename(track_out_file.filename)
                track_out_path = os.path.join(UPLOAD_FOLDER_MUSIC, track_out_filename)
                track_out_file.save(track_out_path)

            # Avatar файл
            avatar_path = None
            avatar_file = request.files.get('avatar_file')
            if avatar_file and avatar_file.filename != '':
                avatar_filename = secure_filename(avatar_file.filename)
                avatar_path = os.path.join(UPLOAD_FOLDER_AVATARS, avatar_filename)
                avatar_file.save(avatar_path)

            # 4. Сохранение в базу данных
            new_music = Music(
                title=title,
                file_path=music_path,
                file_path_wav=music_wav_path,
                file_path_track_out=track_out_path,
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

            db.session.add(new_music)
            db.session.commit()
            
            new_log(f"Трек '{title}' успешно загружен администратором {current_user.username}")
            flash("Трек успешно загружен!")
            return redirect(url_for('main.index'))
            
        except Exception as e:
            db.session.rollback()
            new_log(f"ОШИБКА при загрузке трека: {str(e)}")
            flash(f"Ошибка при загрузке: {str(e)}")
            return redirect(request.url)

    return render_template('upload.html')