from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash


class UserService:
    @staticmethod
    def register_user(username, password, gender, birth_date, full_name):
        existing_user = User.find_by_username(username)
        if existing_user:
            return {'success': False, 'message': 'Пользователь с таким именем уже существует'}

        password_hash = generate_password_hash(password)

        new_user = User(
            username=username,
            password_hash=password_hash,
            gender=gender,
            birth_date=birth_date,
            full_name=full_name
        )

        User.add_user(new_user)

        return {
            'success': True,
            'message': 'Пользователь успешно зарегистрирован',
            'user': new_user.to_dict()
        }

    @staticmethod
    def login_user(username, password):
        user = User.find_by_username(username)

        if not user or not check_password_hash(user.password_hash, password):
            return {'success': False, 'message': 'Неверный логин или пароль'}

        return {
            'success': True,
            'message': 'Вход выполнен успешно',
            'user': user.to_dict()
        }

    @staticmethod
    def get_users(is_authenticated):
        if is_authenticated:
            return {
                'success': True,
                'users': [user.to_dict() for user in User.get_all()]
            }
        else:
            return {
                'success': True,
                'users': User.get_all_usernames()
            }