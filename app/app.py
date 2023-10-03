#!/usr/bin/env python3

from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/pius/Downloads/python-code-challenge-superheroes-1 (1)/python-code-challenge-superheroes/code-challenge/app/db/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return ''

# GET /heroes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    hero_list = []
    for hero in heroes:
        hero_list.append({
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name
        })
    return jsonify(hero_list)

# GET /heroes/:id
@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if hero is None:
        return make_response(jsonify({'error': 'Hero not found'}), 404)

    powers = []
    for power in hero.powers:
        powers.append({
            'id': power.id,
            'name': power.name,
            'description': power.description
        })

    hero_data = {
        'id': hero.id,
        'name': hero.name,
        'super_name': hero.super_name,
        'powers': powers
    }
    return jsonify(hero_data)

# GET /powers
@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    power_list = []
    for power in powers:
        power_list.append({
            'id': power.id,
            'name': power.name,
            'description': power.description
        })
    return jsonify(power_list)

# GET /powers/:id
@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if power is None:
        return make_response(jsonify({'error': 'Power not found'}), 404)
    power_data = {
        'id': power.id,
        'name': power.name,
        'description': power.description
    }
    return jsonify(power_data)

# PATCH /powers/:id
@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if power is None:
        return make_response(jsonify({'error': 'Power not found'}), 404)

    try:
        data = request.get_json()
        if 'description' in data:
            power.description = data['description']
            db.session.commit()
            return jsonify({
                'id': power.id,
                'name': power.name,
                'description': power.description
            })
        else:
            return make_response(jsonify({'errors': ['validation errors']}), 400)
    except Exception as e:
        return make_response(jsonify({'errors': ['validation errors']}), 400)

# POST /hero_powers
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    try:
        data = request.get_json()
        strength = data.get('strength')
        power_id = data.get('power_id')
        hero_id = data.get('hero_id')

        hero = Hero.query.get(hero_id)
        power = Power.query.get(power_id)

        if hero is None or power is None:
            return make_response(jsonify({'error': 'Hero or Power not found'}), 404)

        hero_power = HeroPower(strength=strength, hero=hero, power=power)
        db.session.add(hero_power)
        db.session.commit()

        # Retrieve the updated hero data
        powers = []
        for p in hero.powers:
            powers.append({
                'id': p.id,
                'name': p.name,
                'description': p.description
            })

        hero_data = {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name,
            'powers': powers
        }
        return jsonify(hero_data), 201
    except Exception as e:
        return make_response(jsonify({'errors': ['validation errors']}), 400)

if __name__ == '__main__':
    app.run(port=5555)
