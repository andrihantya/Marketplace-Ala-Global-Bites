from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model database untuk resep resep
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
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    country = db.Column(db.String(50))
    favorites = db.relationship('Recipe', backref='user', lazy=True)

# Inisialisasi database
with app.app_context():
    db.create_all()

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

# Rute untuk mendapatkan resep yang direkomendasikan
@app.route('/recommend', methods=['GET'])
def get_recommendations():
    # Contoh rekomendasi sederhana berdasarkan kategori
    category = request.args.get('category')
    if category:
        recipes = Recipe.query.filter_by(category=category).all()
    else:
        recipes = Recipe.query.all()
    return jsonify([recipe.to_json() for recipe in random.sample(recipes, 5)])

# Rute untuk menambahkan resep baru
@app.route('/recipes', methods=['POST'])
def add_recipe():
    data = request.get_json()
    recipe = Recipe(
        name=data['name'],
        category=data['category'],
        ingredients=data['ingredients'],
        instructions=data['instructions'],
        image_url=data['image_url'],
        country=data['country'],
        rating=data['rating'],
        user_id=1  # Ganti dengan ID pengguna yang benar
    )
    db.session.add(recipe)
    db.session.commit()
    return jsonify({'message': 'Resep berhasil ditambahkan'}), 201

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

if __name__ == '__main__':
    app.run(debug=True)
