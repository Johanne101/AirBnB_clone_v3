#!/usr/bin/python3

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State

@app_views.route('states', methods=['POST, GET'] strict_slashes=False)
def all_states():

@app_views.route('/states/<state_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def state_by_id(state_id):

