from flask import Flask
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session
from sqlalchemy import text
import os
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db = SQLAlchemy()
csrf = CSRFProtect()
migrate = Migrate()
session = Session()

def wait_for_db(app, retries=30, delay=2):
    logger.info("Ожидание готовности базы данных...")
    for i in range(retries):
        try:
            logger.info(f"Попытка подключения {i+1}/{retries}")
            with app.app_context():
                db.session.execute(text('SELECT 1'))
                logger.info("Подключение к базе данных установлено успешно!")
                return True
        except Exception as e:
            logger.warning(f"Не удалось подключиться к базе данных: {e}")
            time.sleep(delay)
    
    logger.error("Не удалось подключиться к базе данных после всех попыток")
    return False

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-12345')

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', 'mysql+pymysql://user:password@db:3306/user_api'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_TYPE'] = 'filesystem'

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    session.init_app(app)

    @app.route('/health')
    def health():
        return {"status": "ok", "time": "2025-04-05 20:21:10", "user": "F1ankerB"}

    @app.after_request
    def add_csrf_token_to_response(response):
        if app.config.get('WTF_CSRF_ENABLED', True):
            response.headers['X-CSRF-Token'] = generate_csrf()
        return response

    from app.controllers.user_controller import user_bp
    app.register_blueprint(user_bp, url_prefix='/api')

    if wait_for_db(app):
        with app.app_context():
            try:
                from app.models.user import User
                db.create_all()
                logger.info("Таблицы базы данных созданы успешно")
            except Exception as e:
                logger.error(f"Ошибка при создании таблиц: {e}")

    return app
