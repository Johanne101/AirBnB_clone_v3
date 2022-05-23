#!/usr/bin/python3

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State
from werkzeug.exceptions import HTTPException


@app_views.route('states', methods=['POST, GET'], strict_slashes=False)
def all_states():
    if request.method == 'POST':
        state_created = None
        try:
            request = request.get_json()
            state_name = request.get('name')
            if state_name is None:
                abort(400, description='Missing name')

            state_created = State(name=state_name)
            state_created.save()
            return jsonify(state_created.to_dict()), 201
        except Exception as e:
            if isinstance(e, HTTPException):
                abort(400, description='Not a JSON')
            else:
                abort(500)

        states = storage.all('State')
        state_list = []
        for state in states.value():
            state_list.append(state.to_dict())
        return jsonify(state_list)


@app_views.route('/states/<state_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def state_by_id(state_id):
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    if request.method == 'DELETE':
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        try:
            request = request.get_json()
            request['created_at'] = state.created_at
            request['id'] = state.id
            state = State(**request)
            state.save()
            return jsonify(state.to_dict()), 200
        except Exception as e:
            if isinstance(e, HTTPException):
                abort(400, description='Not a JSON')
            else:
                abort(500)
    return jsonify(state.to_dict())
