#!/usr/bin/python3
""" Handles HTTP methods """

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.city import City
from werkzeug.exceptions import HTTPException


@app_views.route('states/<state_id>/cities', methods=['POST, GET'],
                 strict_slashes=False)
def all_cities(state_id):
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    if request.method == 'POST':
        city_created = None
        try:
            request = request.get_json()
            city_name = request.get('name')
            if city_name is None:
                abort(400, description='Missing name')

            city_created = City(name=city_name)
            city_created.save()
            return jsonify(city_created.to_dict()), 201
        except Exception as e:
            abort(400, description='Not a JSON')

    cities = storage.all('City')
    city_list = []
    for city in cities.value():
        city_list.append(city.to_dict())
    return jsonify(city_list)


@app_views.route('/cities/<city_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def city_by_id(city_id):
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        try:
            request = request.get_json()
            request['created_at'] = city.created_at
            request['id'] = city.id
            city = City(**request)
            city.save()
            return jsonify(city.to_dict()), 200
        except Exception as e:
            abort(400, description='Not a JSON')
    return jsonify(city.to_dict())
