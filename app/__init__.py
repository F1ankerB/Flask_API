from flask import Flask
from flask_wtf.csrf import CSRFProtect
from config import Config
from flask_wtf.csrf import generate_csrf
csrf = CSRFProtect()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    csrf.init_app(app)

    @app.after_request
    def add_csrf_token_to_response(response):
        response.headers['X-CSRF-Token'] = generate_csrf()
        return response

    from app.controllers.user_controller import user_bp
    app.register_blueprint(user_bp, url_prefix='/api')

    return app