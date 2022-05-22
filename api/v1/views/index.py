#!/usr/bin/python3
""" Cretes route for /status/ on object app_views """


from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_viewsroute('/status', strict_slashes=False)
def status():
    return jsonify({"status": OK})
