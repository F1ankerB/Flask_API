import os
import secrets


class Config:
    SECRET_KEY = secrets.token_hex(16)

    DATABASE_PATH = os.path.join(os.getcwd(), 'users.db')

    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = 3600