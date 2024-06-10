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

# Model database untuk komentar
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Model database untuk pengguna
class User(db.Model):
    # ... (Sama seperti sebelumnya)

# Dekorator untuk memeriksa token JWT
# ... (Sama seperti sebelumnya)

# Rute untuk mendapatkan komentar pada resep
@app.route('/recipes/<int:recipe_id>/comments', methods=['GET'])
def get_comments(recipe_id):
    comments = Comment.query.filter_by(recipe_id=recipe_id).all()
    return jsonify([comment.to_json() for comment in comments])

# Rute untuk menambahkan komentar pada resep
@app.route('/recipes/<int:recipe_id>/comments', methods=['POST'])
@token_required
def add_comment(current_user, recipe_id):
    data = request.get_json()
    comment = Comment(
        content=data['content'],
        recipe_id=recipe_id,
        user_id=current_user.id
    )
    db.session.add(comment)
    db.session.commit()
    return jsonify({'message': 'Komentar berhasil ditambahkan'}), 201

# Rute untuk menghapus komentar
@app.route('/comments/<int:comment_id>', methods=['DELETE'])
@token_required
def delete_comment(current_user, comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized'}), 401
    db.session.delete(comment)
    db.session.commit()
    return jsonify({'message': 'Komentar berhasil dihapus'}), 204

# Menambahkan metode to_json ke model Comment
Comment.to_json = lambda self: {
    'id': self.id,
    'content': self.content,
    'user_id': self.user_id
}

# Inisialisasi database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
