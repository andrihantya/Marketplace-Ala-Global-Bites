from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model database untuk pengguna
class User(db.Model):
    # ... (Sama seperti sebelumnya)

# Dekorator untuk memeriksa token JWT
# ... (Sama seperti sebelumnya)

# Rute untuk mendapatkan profil pengguna
@app.route('/users/<int:user_id>', methods=['GET'])
@token_required
def get_user_profile(current_user, user_id):
    if current_user.id != user_id:
        return jsonify({'message': 'Unauthorized'}), 401
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_json())

# Rute untuk memperbarui profil pengguna
@app.route('/users/<int:user_id>', methods=['PUT'])
@token_required
def update_user_profile(current_user, user_id):
    if current_user.id != user_id:
        return jsonify({'message': 'Unauthorized'}), 401
    data = request.get_json()
    user = User.query.get_or_404(user_id)
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    user.country = data.get('country', user.country)
    db.session.commit()
    return jsonify({'message': 'Profile updated successfully'}), 200

# Menambahkan metode to_json ke model User
User.to_json = lambda self: {
    'id': self.id,
    'username': self.username,
    'email': self.email,
    'country': self.country
}

# Inisialisasi database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
