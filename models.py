from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Инициализируем БД без привязки к конкретному приложению сразу
db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<User {self.username}>'
    

class Music(db.Model):
    __tablename__ = 'music'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    avatar_path = db.Column(db.String(500), nullable=True)
    price_mp3 = db.Column(db.Float, nullable=True)
    price_wav = db.Column(db.Float, nullable=True)
    price_track_out = db.Column(db.Float, nullable=True)
    price_exclusive = db.Column(db.Float, nullable=True)
    genre = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    bpm = db.Column(db.Integer, nullable=True)
    key = db.Column(db.String(20), nullable=True)

    
    def __repr__(self):
        return f'<Music {self.title}>'


