from flask import jsonify
import jwt
import datetime
from functools import wraps

def token_required(func):
    """Dekorator untuk memeriksa token JWT."""
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.get(data['user_id'])
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        return func(current_user, *args, **kwargs)
    return decorated

def generate_token(user_id):
    """Membuat token JWT untuk pengguna."""
    token = jwt.encode(
        {'user_id': user_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
        app.config['SECRET_KEY']
    )
    return token.decode('UTF-8')

def handle_error(error, code=400):
    """Menangani kesalahan dan mengembalikan pesan JSON."""
    return jsonify({'message': str(error)}), code
