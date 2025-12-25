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
    

    def __repr__(self):
        return f'<User {self.username}>'