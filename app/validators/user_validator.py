import re
from functools import wraps
from flask import request, jsonify


def validate_username(username):
    pattern = r'^[a-zA-Z0-9]+$'
    return bool(re.match(pattern, username))


def validate_password(password):
    return len(password) >= 8


def validate_login_data():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json()

            if not data or 'username' not in data or 'password' not in data:
                return jsonify({
                    'success': False,
                    'message': 'Отсутствуют обязательные поля: логин и пароль'
                }), 400

            if not validate_username(data['username']):
                return jsonify({
                    'success': False,
                    'message': 'Логин должен содержать только английские буквы и цифры'
                }), 400

            if not validate_password(data['password']):
                return jsonify({
                    'success': False,
                    'message': 'Пароль должен быть не менее 8 символов'
                }), 400

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def validate_registration_data():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json()

            if not data:
                return jsonify({
                    'success': False,
                    'message': 'Данные не предоставлены'
                }), 400

            required_fields = ['username', 'password', 'gender', 'birth_date', 'full_name']
            missing_fields = [field for field in required_fields if field not in data]

            if missing_fields:
                return jsonify({
                    'success': False,
                    'message': f'Отсутствуют обязательные поля: {", ".join(missing_fields)}'
                }), 400

            if not validate_username(data['username']):
                return jsonify({
                    'success': False,
                    'message': 'Логин должен содержать только английские буквы и цифры'
                }), 400

            if not validate_password(data['password']):
                return jsonify({
                    'success': False,
                    'message': 'Пароль должен быть не менее 8 символов'
                }), 400

            return f(*args, **kwargs)

        return decorated_function

    return decorator