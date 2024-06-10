from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model database untuk resep
class Recipe(db.Model):
    # ... (Sama seperti sebelumnya)

# Model database untuk pengguna
class User(db.Model):
    # ... (Sama seperti sebelumnya)
    favorites = db.relationship('Recipe', backref='user', lazy=True)

# Dekorator untuk memeriksa token JWT
def token_required(func):
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

# Rute untuk menambahkan resep ke favorit
@app.route('/favorites/<int:recipe_id>', methods=['POST'])
@token_required
def add_favorite(current_user, recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    current_user.favorites.append(recipe)
    db.session.commit()
    return jsonify({'message': 'Recipe added to favorites'}), 201

# Rute untuk menghapus resep dari favorit
@app.route('/favorites/<int:recipe_id>', methods=['DELETE'])
@token_required
def remove_favorite(current_user, recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    current_user.favorites.remove(recipe)
    db.session.commit()
    return jsonify({'message': 'Recipe removed from favorites'}), 204

# ... (Rute lainnya seperti sebelumnya)

# Inisialisasi database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
