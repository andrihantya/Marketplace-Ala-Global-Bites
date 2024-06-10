from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model database untuk resep
class Recipe(db.Model):
    # ... (Sama seperti sebelumnya)

# Rute untuk mendapatkan rekomendasi resep
@app.route('/recommend', methods=['GET'])
def get_recommendations():
    # Contoh rekomendasi sederhana berdasarkan kategori
    category = request.args.get('category')
    if category:
        recipes = Recipe.query.filter_by(category=category).all()
    else:
        recipes = Recipe.query.all()
    return jsonify([recipe.to_json() for recipe in random.sample(recipes, 5)])

# ... (Rute lainnya seperti sebelumnya)

# Inisialisasi database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
