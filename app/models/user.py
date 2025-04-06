from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    gender = db.Column(db.String(10), nullable=True)
    birth_date = db.Column(db.String(10), nullable=True)
    full_name = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, username, password, gender=None, birth_date=None, full_name=None):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.gender = gender
        self.birth_date = birth_date
        self.full_name = full_name
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
