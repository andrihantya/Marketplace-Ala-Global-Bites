import unittest
from app import app, db, Recipe, User
import json

class TestAPI(unittest.TestCase):

    def setUp(self):
        """Menjalankan sebelum setiap tes."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        """Menjalankan setelah setiap tes."""
        db.session.remove()
        db.drop_all()

    def test_get_recipes(self):
        """Menguji rute untuk mendapatkan semua resep."""
        response = self.app.get('/recipes')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(json.loads(response.data), list)

    def test_get_recipe_by_id(self):
        """Menguji rute untuk mendapatkan resep berdasarkan ID."""
        recipe = Recipe(
            name="Spaghetti Carbonara",
            category="Italian",
            ingredients="Spaghetti, eggs, pancetta, Parmesan cheese, black pepper",
            instructions="Cook spaghetti al dente. In a bowl, whisk eggs, Parmesan cheese, and black pepper. Drain spaghetti and toss with egg mixture. Add pancetta and serve.",
            image_url="https://www.example.com/spaghetti-carbonara.jpg",
            country="Italy",
            rating=4.5
        )
        db.session.add(recipe)
        db.session.commit()
        recipe_id = recipe.id

        response = self.app.get(f'/recipes/{recipe_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['id'], recipe_id)

    # Tambahkan tes untuk rute lainnya di sini...

    # Contoh tes untuk login
    def test_login(self):
        """Menguji rute untuk login."""
        user = User(
            username="user1",
            email="user1@example.com",
            password="password123"
        )
        db.session.add(user)
        db.session.commit()

        response = self.app.post(
            '/login',
            data=json.dumps({'username': 'user1', 'password': 'password123'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', json.loads(response.data))

    # Tambahkan tes untuk fitur lainnya seperti registrasi, menambahkan resep, memberikan rating, dll.

if __name__ == '__main__':
    unittest.main()
