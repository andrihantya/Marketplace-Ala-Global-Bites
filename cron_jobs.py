import time
from app import db, Recipe

def update_recipe_ratings():
    """Memperbarui rating resep berdasarkan komentar baru."""
    # 1. Dapatkan semua resep yang memiliki komentar baru
    # 2. Hitung rata-rata rating untuk setiap resep
    # 3. Perbarui kolom 'rating' pada objek resep
    # 4. Simpan perubahan ke database

    # Contoh sederhana:
    for recipe in Recipe.query.all():
        recipe.rating = 4.0  # Hitung rating sebenarnya berdasarkan komentar
        db.session.commit()

    print("Rating resep berhasil diperbarui!")

if __name__ == "__main__":
    while True:
        update_recipe_ratings()
        time.sleep(3600)  # Jalankan cron job setiap jam
