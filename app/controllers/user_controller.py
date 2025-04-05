from flask import Blueprint, request, jsonify, session
from functools import wraps
from app.services.user_service import UserService
from app.validators.user_validator import validate_login_data, validate_registration_data

user_bp = Blueprint('user', __name__)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({
                'success': False,
                'message': 'Требуется авторизация'
            }), 401
        return f(*args, **kwargs)

    return decorated_function


@user_bp.route('/get_users', methods=['GET'])
def get_users():
    is_authenticated = 'user_id' in session

    result = UserService.get_users(is_authenticated)

    return jsonify(result)


@user_bp.route('/login_user', methods=['POST'])
@validate_login_data()
def login_user():
    data = request.get_json()
    username = data['username']
    password = data['password']

    result = UserService.login_user(username, password)

    if result['success']:
        # Сохранение в сессию
        session['user_id'] = username

    return jsonify(result)


@user_bp.route('/register_user', methods=['POST'])
@validate_registration_data()
def register_user():
    data = request.get_json()

    username = data['username']
    password = data['password']
    gender = data['gender']
    birth_date = data['birth_date']
    full_name = data['full_name']

    result = UserService.register_user(
        username, password, gender, birth_date, full_name
    )

    return jsonify(result)


@user_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({
        'success': True,
        'message': 'Выход выполнен успешно'
    })