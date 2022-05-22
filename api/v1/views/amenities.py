#!/usr/bin/python3

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity

@app_views.route('amenities', methods=['POST, GET'] strict_slashes=False)
def all_amenities():

@app_views.route('/amenities/<amenity_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def amenity_by_id(amenity_id):

