#!/usr/bin/python3
""" Cretes route for /status/ on object app_views """


from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    return jsonify({"status": OK})

@app_views.route('stats', strict_slashes=False)
def stats():
    classes = {"Amenity": "amenities", "City": "cities", "Place": "places",
               "Review": "reviews", "State": "states", "User": "users"}

    objs = {}

    for key, value in objs.items():
        total = storage.count(key)
        objs[value] = total
    objs = jsonify(objs)
    return objs

