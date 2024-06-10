from app import db, Recipe, User

# Data resep awal
recipes = [
    {
        "name": "Spaghetti Carbonara",
        "category": "Italian",
        "ingredients": "Spaghetti, eggs, pancetta, Parmesan cheese, black pepper",
        "instructions": "Cook spaghetti al dente. In a bowl, whisk eggs, Parmesan cheese, and black pepper. Drain spaghetti and toss with egg mixture. Add pancetta and serve.",
        "image_url": "https://www.example.com/spaghetti-carbonara.jpg",
        "country": "Italy",
        "rating": 4.5
    },
    {
        "name": "Chicken Tikka Masala",
        "category": "Indian",
        "ingredients": "Chicken, yogurt, spices (garam masala, turmeric, ginger), onions, tomatoes, cream",
        "instructions": "Marinate chicken in yogurt and spices. Grill or bake chicken. Make a sauce with onions, tomatoes, and spices. Add cream and cooked chicken. Serve with rice.",
        "image_url": "https://www.example.com/chicken-tikka-masala.jpg",
        "country": "India",
        "rating": 4.0
    },
    # Tambahkan lebih banyak data resep di sini...
]

# Data pengguna awal
users = [
    {
        "username": "user1",
        "email": "user1@example.com",
        "password": "password123"
    },
    {
        "username": "user2",
        "email": "user2@example.com",
        "password": "password456"
    },
    # Tambahkan lebih banyak data pengguna di sini...
]

# Fungsi untuk menambahkan resep ke database
def add_recipes(recipes):
    for recipe_data in recipes:
        recipe = Recipe(
            name=recipe_data["name"],
            category=recipe_data["category"],
            ingredients=recipe_data["ingredients"],
            instructions=recipe_data["instructions"],
            image_url=recipe_data["image_url"],
            country=recipe_data["country"],
            rating=recipe_data["rating"]
        )
        db.session.add(recipe)

# Fungsi untuk menambahkan pengguna ke database
def add_users(users):
    for user_data in users:
        user = User(
            username=user_data["username"],
            email=user_data["email"],
            password=user_data["password"]
        )
        db.session.add(user)

# Menjalankan script untuk mengisi data awal
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        add_recipes(recipes)
        add_users(users)
        db.session.commit()
        print("Data awal berhasil diisi!")
