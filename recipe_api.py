from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model database untuk resep
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200))
    country = db.Column(db.String(50))
    rating = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# Model database untuk pengguna
class User(db.Model):
    # ... (Sama seperti sebelumnya)

# Dekorator untuk memeriksa token JWT
# ... (Sama seperti sebelumnya)

# Rute untuk mendapatkan semua resep
@app.route('/recipes', methods=['GET'])
def get_recipes():
    recipes = Recipe.query.all()
    return jsonify([recipe.to_json() for recipe in recipes])

# Rute untuk mendapatkan resep berdasarkan ID
@app.route('/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return jsonify(recipe.to_json())

# Rute untuk menambahkan resep baru
@app.route('/recipes', methods=['POST'])
@token_required
def add_recipe(current_user):
    data = request.get_json()
    recipe = Recipe(
        name=data['name'],
        category=data['category'],
        ingredients=data['ingredients'],
        instructions=data['instructions'],
        image_url=data['image_url'],
        country=data['country'],
        rating=data['rating'],
        user_id=current_user.id
    )
    db.session.add(recipe)
    db.session.commit()
    return jsonify({'message': 'Resep berhasil ditambahkan'}), 201

# Rute untuk memperbarui resep
@app.route('/recipes/<int:recipe_id>', methods=['PUT'])
@token_required
def update_recipe(current_user, recipe_id):
    data = request.get_json()
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 401
    recipe.name = data['name']
    recipe.category = data['category']
    recipe.ingredients = data['ingredients']
    recipe.instructions = data['instructions']
    recipe.image_url = data['image_url']
    recipe.country = data['country']
    recipe.rating = data['rating']
    db.session.commit()
    return jsonify({'message': 'Resep berhasil diperbarui'}), 200

# Rute untuk menghapus resep
@app.route('/recipes/<int:recipe_id>', methods=['DELETE'])
@token_required
def delete_recipe(current_user, recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 401
    db.session.delete(recipe)
    db.session.commit()
    return jsonify({'message': 'Resep berhasil dihapus'}), 204

# Menambahkan metode to_json ke model Recipe
Recipe.to_json = lambda self: {
    'id': self.id,
    'name': self.name,
    'category': self.category,
    'ingredients': self.ingredients,
    'instructions': self.instructions,
    'image_url': self.image_url,
    'country': self.country,
    'rating': self.rating
}

# Inisialisasi database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
