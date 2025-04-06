from flask import Blueprint, request, jsonify, session
from app.models.user import User
from app import db
from sqlalchemy import text

user_bp = Blueprint('user', __name__)

@user_bp.route('/register_user', methods=['POST'])
def register_user():
    data = request.json
    
    username = data.get('username')
    password = data.get('password')
    gender = data.get('gender')
    birth_date = data.get('birth_date')
    full_name = data.get('full_name')
    
    if not username or not password:
        return jsonify({'success': False, 'message': 'Требуется логин и пароль'}), 400
        
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'success': False, 'message': 'Пользователь с таким именем уже существует'}), 400
        
    user = User(username=username, password=password, gender=gender, 
                birth_date=birth_date, full_name=full_name)
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Пользователь успешно зарегистрирован'})

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'success': False, 'message': 'Требуется логин и пароль'}), 400
    
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'success': False, 'message': 'Пользователь не найден'}), 401
        
    if not user.check_password(password):
        return jsonify({'success': False, 'message': 'Неверный пароль'}), 401
    
    session['user_id'] = user.id
    session['logged_in'] = True
    
    return jsonify({'success': True, 'message': 'Авторизация успешна'})

@user_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    session.pop('logged_in', None)
    
    return jsonify({'success': True, 'message': 'Выход успешно выполнен'})

@user_bp.route('/get_users', methods=['GET'])
def get_users():
    is_authenticated = 'logged_in' in session and session['logged_in']
    users = User.query.all()
    
    if is_authenticated:
        result = [{
            'username': user.username, 
            'full_name': user.full_name,
            'gender': user.gender,
            'birth_date': user.birth_date
        } for user in users]
    else:
        result = [{'username': user.username} for user in users]
    
    return jsonify({
        'success': True,
        'users': result
    })

@user_bp.route('/db_test', methods=['GET'])
def db_test():
    try:
        result = db.session.execute(text('SELECT 1')).fetchone()
        databases = db.session.execute(text('SHOW DATABASES')).fetchall()
        
        return jsonify({
            "status": "ok", 
            "connected": True, 
            "result": str(result),
            "databases": [db[0] for db in databases]
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
