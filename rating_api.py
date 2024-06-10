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

# Dekorator untuk memeriksa token JWT
# ... (Sama seperti sebelumnya)

# Rute untuk memberikan rating pada resep
@app.route('/recipes/<int:recipe_id>/rating', methods=['POST'])
@token_required
def rate_recipe(current_user, recipe_id):
    data = request.get_json()
    rating = data['rating']
    recipe = Recipe.query.get_or_404(recipe_id)
    recipe.rating = rating
    db.session.commit()
    return jsonify({'message': 'Recipe rated successfully'}), 200

# ... (Rute lainnya seperti sebelumnya)

# Inisialisasi database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
