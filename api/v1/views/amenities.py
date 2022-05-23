#!/usr/bin/python3

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from werkzeug.exceptions import HTTPException


@app_views.route('amenities', methods=['POST, GET'], strict_slashes=False)
def all_amenities():
    if request.method == 'POST':
        amenity_created = None
        try:
            request = request.get_json()
            amenity_name = request.get('name')
            if amenity_name is None:
                abort(400, description='Missing name')

            amenity_created = Amenity(name=amenity_name)
            amenity_created.save()
            return jsonify(amenity_created.to_dict()), 201
        except Exception as e:
            abort(400, description='Not a JSON')

        amenities = storage.all('Amenity')
        amenity_list = []
        for amenity in amenities.value():
            amenity_list.append(amenity.to_dict())
        return jsonify(amenity_list)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def amenity_by_id(amenity_id):
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    if request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        try:
            request = request.get_json()
            request['created_at'] = amenity.created_at
            request['id'] = amenity.id
            amenity = Amenity(**request)
            amenity.save()
            return jsonify(amenity.to_dict()), 200
        except Exception as e:
            abort(400, description='Not a JSON')
    return jsonify(amenity.to_dict())
