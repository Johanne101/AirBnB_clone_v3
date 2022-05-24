#!/usr/bin/python3
""" Handles HTTP methods """

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from werkzeug.exceptions import HTTPException


@app_views.route('places', methods=['POST, GET'], strict_slashes=False)
def all_places(city_id):
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    if request.method == 'POST':
        place_name = None
        user_id = None
        try:
            request = request.get_json()
            place_name = request.get('name')
            place_user_id = request_dict.get('user_id')
        except Exception as e:
            abort(400, description='Not a JSON')
        if place_name is None:
            abort(400, description='Missing name')
        if place_user_id is None:
            abort(400, description='Missing user_id')
        user = storage.get('User', user_id)
        if user is None:
            abort(404)
        place_created = Place(name=place_name, place_user_id=user_id,
                              city_id=city_id)

        place_created.save()
        return jsonify(new_places.to_dict()), 201

    place_list = []
    for place in city.places():
        place_list.append(place.to_dict())
    return jsonify(place_list)


@app_views.route('/places/<place_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def place_by_id(place_id):
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        try:
            request = request.get_json()
            request['created_at'] = place.created_at
            request['user_id'] = place.id
            request['city_id'] = place.city_id
            request['updated_at'] = place.updated_at
            request['id'] = place.id
            place = Place(**request)
            place.save()
            return jsonify(place.to_dict()), 200
        except Exception as e:
            abort(400, description='Not a JSON')
    return jsonify(place.to_dict())
