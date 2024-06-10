from flask import Flask, jsonify
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app, version='1.0', title='Recipe API', description='API untuk website resep')

# Model untuk resep
recipe_model = api.model('Recipe', {
    'id': fields.Integer(readOnly=True, description='ID resep'),
    'name': fields.String(required=True, description='Nama resep'),
    'category': fields.String(required=True, description='Kategori resep'),
    'ingredients': fields.String(required=True, description='Bahan-bahan resep'),
    'instructions': fields.String(required=True, description='Instruksi resep'),
    'image_url': fields.String(required=True, description='URL gambar resep'),
    'country': fields.String(required=True, description='Negara asal resep'),
    'rating': fields.Float(required=True, description='Rating resep'),
})

# Rute untuk mendapatkan semua resep
@api.route('/recipes')
class RecipeList(Resource):
    @api.doc(description='Get all recipes')
    @api.marshal_list_with(recipe_model)
    def get(self):
        # Kode untuk mengambil semua resep
        return []

# Rute untuk mendapatkan resep berdasarkan ID
@api.route('/recipes/<int:recipe_id>')
class RecipeItem(Resource):
    @api.doc(description='Get a recipe by ID')
    @api.marshal_with(recipe_model)
    def get(self, recipe_id):
        # Kode untuk mengambil resep berdasarkan ID
        return {}

if __name__ == '__main__':
    app.run(debug=True)
