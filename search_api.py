from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model database untuk resep
class Recipe(db.Model):
    # ... (Sama seperti sebelumnya)

# Rute untuk mencari resep
@app.route('/search', methods=['GET'])
def search_recipes():
    query = request.args.get('q')
    if query:
        recipes = Recipe.query.filter(
            Recipe.name.ilike(f'%{query}%') |
            Recipe.ingredients.ilike(f'%{query}%')
        ).all()
    else:
        recipes = Recipe.query.all()
    return jsonify([recipe.to_json() for recipe in recipes])

# ... (Rute lainnya seperti sebelumnya)

# Inisialisasi database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
