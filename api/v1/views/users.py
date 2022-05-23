#!/usr/bin/python3

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.user import User
from werkzeug.exceptions import HTTPException


@app_views.route('users', methods=['POST, GET'], strict_slashes=False)
def all_users():
    if request.method == 'POST':
        user_created = None
        try:
            request = request.get_json()
            user_name = request.get('name')
            if user_name is None:
                abort(400, description='Missing name')

            user_created = User(name=user_name)
            user_created.save()
            return jsonify(user_created.to_dict()), 201
        except Exception as e:
            if isinstance(e, HTTPException):
                abort(400, description='Not a JSON')
            else:
                abort(500)

        users = storage.all('User')
        user_list = []
        for user in users.value():
            user_list.append(user.to_dict())
        return jsonify(user_list)


@app_views.route('/users/<user_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def user_by_id(user_id):
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    if request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        try:
            request = request.get_json()
            request['created_at'] = user.created_at
            request['id'] = user.id
            user = User(**request)
            user.save()
            return jsonify(user.to_dict()), 200
        except Exception as e:
            if isinstance(e, HTTPException):
                abort(400, description='Not a JSON')
            else:
                abort(500)
    return jsonify(user.to_dict())
