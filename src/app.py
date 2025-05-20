"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planets, People, Starship, Favorites


app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = []

    for user in users:
        users_list.append({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "favorites": [fav.serialize() for fav in user.favorites]
        })

    return jsonify(users_list), 200






@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data provided"}), 400

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "Missing name, email, or password"}), 400

    new_user = User(name=name, email=email, password=password, is_active=True)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "User created successfully",
        "user": new_user.serialize()
    }), 201






@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_by_id(planet_id):
    planet = Planets.query.get(planet_id)
    if not planet:
        return jsonify({"error": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200







@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    return jsonify([person.serialize() for person in people]), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person_by_id(people_id):
    person = People.query.get(people_id)
    if not person:
        return jsonify({"error": "Person not found"}), 404
    return jsonify(person.serialize()), 200







@app.route('/starships', methods=['GET'])
def get_starships():
    starships = Starship.query.all()
    return jsonify([ship.serialize() for ship in starships]), 200

@app.route('/starships/<int:starship_id>', methods=['GET'])
def get_starship_by_id(starship_id):
    ship = Starship.query.get(starship_id)
    if not ship:
        return jsonify({"error": "Starship not found"}), 404
    return jsonify(ship.serialize()), 200







@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    favorites_list = [fav.serialize() for fav in user.favorites]
    return jsonify(favorites_list), 200








@app.route('/users/<int:user_id>/favorite/planet/<int:planet_id>', methods=['POST'])
def add_planet_to_favorites(user_id, planet_id):
    if not User.query.get(user_id) or not Planets.query.get(planet_id):
        return jsonify({"error": "User or Planet not found"}), 404

    exists = Favorites.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if exists:
        return jsonify({"message": "Planet already in favorites"}), 400

    new_fav = Favorites(user_id=user_id, planet_id=planet_id)
    db.session.add(new_fav)
    db.session.commit()
    return jsonify({"message": "Planet added to favorites", "favorite": new_fav.serialize()}), 201







@app.route('/users/<int:user_id>/favorite/planet/<int:planet_id>', methods=['DELETE'])
def remove_planet_from_favorites(user_id, planet_id):
    favorite = Favorites.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if not favorite:
        return jsonify({"error": "Planet is not in favorites"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": "Planet removed from favorites"}), 200








@app.route('/users/<int:user_id>/favorite/people/<int:people_id>', methods=['POST'])
def add_people_to_favorites(user_id, people_id):
    if not User.query.get(user_id) or not People.query.get(people_id):
        return jsonify({"error": "User or Person not found"}), 404

    exists = Favorites.query.filter_by(user_id=user_id, people_id=people_id).first()
    if exists:
        return jsonify({"message": "Person already in favorites"}), 400

    new_fav = Favorites(user_id=user_id, people_id=people_id)
    db.session.add(new_fav)
    db.session.commit()
    return jsonify({"message": "Person added to favorites", "favorite": new_fav.serialize()}), 201






@app.route('/users/<int:user_id>/favorite/people/<int:people_id>', methods=['DELETE'])
def remove_people_from_favorites(user_id, people_id):
    favorite = Favorites.query.filter_by(user_id=user_id, people_id=people_id).first()
    if not favorite:
        return jsonify({"error": "Person is not in favorites"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": "Person removed from favorites"}), 200







@app.route('/users/<int:user_id>/favorite/starship/<int:starship_id>', methods=['POST'])
def add_starship_to_favorites(user_id, starship_id):
    if not User.query.get(user_id) or not Starship.query.get(starship_id):
        return jsonify({"error": "User or Starship not found"}), 404

    exists = Favorites.query.filter_by(user_id=user_id, starship_id=starship_id).first()
    if exists:
        return jsonify({"message": "Starship already in favorites"}), 400

    new_fav = Favorites(user_id=user_id, starship_id=starship_id)
    db.session.add(new_fav)
    db.session.commit()
    return jsonify({"message": "Starship added to favorites", "favorite": new_fav.serialize()}), 201







@app.route('/users/<int:user_id>/favorite/starship/<int:starship_id>', methods=['DELETE'])
def remove_starship_from_favorites(user_id, starship_id):
    favorite = Favorites.query.filter_by(user_id=user_id, starship_id=starship_id).first()
    if not favorite:
        return jsonify({"error": "Starship is not in favorites"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": "Starship removed from favorites"}), 200





# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
