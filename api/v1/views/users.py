#!/usr/bin/python3
""" Handles HTTP methods """

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.user import User
from werkzeug.exceptions import HTTPException


@app_views.route('users', methods=['POST, GET'], strict_slashes=False)
def all_users():
    if request.method == 'POST':
        new_email = None
        new_password = None
        try:
            request = request.get_json()
            new_email = request.get('email')
            new_password = request.get('password')
        except Exception as e:
            abort(400, description='Not a JSON')
        if new_email is None:
            abort(400, description='Missing email')
        if new_password is None:
            abort(400, description='Missing password')
        new_user = User(email=new_email, password=new_password)
        new_user.save()

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
            request['updated_at'] = user.updated_at
            request['email'] = user.email
            request['id'] = user.id
            user = User(**request)
            user.save()
            return jsonify(user.to_dict()), 200
        except Exception as e:
            abort(400, description='Not a JSON')
    return jsonify(user.to_dict())
