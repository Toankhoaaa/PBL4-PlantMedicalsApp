# app/routes.py
from flask import Blueprint, jsonify, request
from .models import Plant, MedicinalUse
from .extensions import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return "hello world!!!!"

@main.route('/plants', methods=['GET'])
def get_plants():
    plants = Plant.query.all()
    return jsonify([{
        "plant_id": plant.plant_id,
        "name": plant.name,
        "scientific_name": plant.scientific_name,
        "description": plant.description,
        "family": plant.family
    } for plant in plants])

@main.route('/plants/<int:plant_id>', methods=['GET'])
def get_plant(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    return jsonify({
        "plant_id": plant.plant_id,
        "name": plant.name,
        "scientific_name": plant.scientific_name,
        "description": plant.description,
        "family": plant.family
    })

@main.route('/plants', methods=['POST'])
def add_plant():
    data = request.get_json()
    new_plant = Plant(
        name=data.get('name'),
        scientific_name=data.get('scientific_name'),
        description=data.get('description'),
        family=data.get('family')
    )
    db.session.add(new_plant)
    db.session.commit()
    return jsonify({"message": "Plant added successfully!"}), 201
