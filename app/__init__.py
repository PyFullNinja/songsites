import os
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from .models import db, User  # Точка означает импорт из текущего пакета
from .config import CRYPTO_BOT_TOKEN, UPLOAD_FOLDER_MUSIC, UPLOAD_FOLDER_AVATARS

# Инициализируем объекты расширений без привязки к конкретному app
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__,
                template_folder='../templates', 
                static_folder='../static')
    
    # Конфигурация
    app.config['SECRET_KEY'] = 'dev-key-123'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER_MUSIC'] = UPLOAD_FOLDER_MUSIC
    app.config['UPLOAD_FOLDER_AVATARS'] = UPLOAD_FOLDER_AVATARS
    app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500 Мегабайт)

    # Привязываем расширения к приложению
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login' # Указываем на Blueprint авторизации

    # Создаем папки, если их нет
    os.makedirs(UPLOAD_FOLDER_MUSIC, exist_ok=True)
    os.makedirs(UPLOAD_FOLDER_AVATARS, exist_ok=True)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Регистрация Blueprints (чертежей)
    # Мы разделим логику на основные страницы и авторизацию
    from .routes.main import main_bp
    from .routes.auth import auth_bp
    from .routes.shop import shop_bp
    from .routes.contacts import contacts_bp
    from .routes.upload import upload_bp
    from .routes.admin_panel import admin_panel_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(shop_bp, url_prefix='/shop')
    app.register_blueprint(contacts_bp, url_prefix='/contacts')
    app.register_blueprint(upload_bp, url_prefix='/upload')
    app.register_blueprint(admin_panel_bp, url_prefix='/admin_panel')

    return app