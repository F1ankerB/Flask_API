from datetime import datetime
import json


class User:
    users_db = []

    def __init__(self, username, password_hash, gender=None, birth_date=None, full_name=None):
        self.username = username
        self.password_hash = password_hash
        self.gender = gender
        self.birth_date = birth_date
        self.full_name = full_name
        self.created_at = datetime.now().isoformat()

    def to_dict(self, include_password=False):
        user_dict = {
            'username': self.username,
            'gender': self.gender,
            'birth_date': self.birth_date,
            'full_name': self.full_name,
            'created_at': self.created_at
        }

        if include_password:
            user_dict['password_hash'] = self.password_hash

        return user_dict

    @classmethod
    def find_by_username(cls, username):
        for user in cls.users_db:
            if user.username == username:
                return user
        return None

    @classmethod
    def get_all(cls):
        return cls.users_db

    @classmethod
    def get_all_usernames(cls):
        return [{'username': user.username} for user in cls.users_db]

    @classmethod
    def add_user(cls, user):
        cls.users_db.append(user)