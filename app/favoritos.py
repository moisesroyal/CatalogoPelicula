from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///favorites.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo para la tabla de favoritos
class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), nullable=False)
    movie_name = db.Column(db.String(120), nullable=False)
    movie_category = db.Column(db.String(80), nullable=False)
    movie_link = db.Column(db.String(200), nullable=False)
    movie_image = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

# Ruta para añadir a favoritos
@app.route('/favorites', methods=['POST'])
def add_favorite():
    data = request.json
    new_favorite = Favorite(
        user_id=data['user_id'],
        movie_name=data['movie_name'],
        movie_category=data['movie_category'],
        movie_link=data['movie_link'],
        movie_image=data['movie_image']
    )
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"message": "Película añadida a favoritos"}), 201

# Ruta para listar favoritos
@app.route('/favorites/<user_id>', methods=['GET'])
def get_favorites(user_id):
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    return render_template('favoritos.html', favorites=favorites)

# Ruta para eliminar un favorito
@app.route('/favorites/delete/<int:id>', methods=['POST'])
def delete_favorite(id):
    favorite = Favorite.query.get_or_404(id)
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": "Película eliminada de favoritos"})
