import os
import requests
from flask import Flask, render_template, redirect, url_for, request, flash

from werkzeug.utils import secure_filename
from models import db, User
from models import *
from flask_migrate import Migrate
from config import *
from telegram_bot import send


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-key-123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)



os.makedirs(UPLOAD_FOLDER_MUSIC, exist_ok=True)
os.makedirs(UPLOAD_FOLDER_AVATARS, exist_ok=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




# --- Маршруты (Routes) ---


#@app.route('/admin')
#@login_required
#def admin():
    #if not current_user.is_admin:
        #User.query.get_or_404(current_user.id).is_admin = True
        #db.session.commit()
    #return redirect(url_for('index'))







# Настройки папок для загрузки (можно вынести в config)

















if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)