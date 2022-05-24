#!/usr/bin/python3
""" Handles HTTP methods """

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.review import Review
from werkzeug.exceptions import HTTPException


@app_views.route('/places/<place_id>/reviews', methods=['POST, GET'],
                 strict_slashes=False)
def all_reviews(place_id):
    place = storage.get('Place', place_id)

    if place is None:
        abort(404)
    if request.method == 'POST':
        review_created = None
        request = None
        try:
            request = request.get_json()
            review_created = request.get('text')
        except Exception as e:
            abort(400, description='Not a JSON')
        user_id = request.get('user_id')
        if user_id is None:
            abort(400, description='Missing user_id')
        user = storage.get('User', user_id)

        if user is None:
            abort(404)
        if review_created is None:
            abort(400, description='Missing text')
        full_review = Review(text=review_created, place_id=place_id,
                             user_id=user_id)
        full_review.save()
        return jsonify(new_review.to_dict()), 201
    review_list = [rev.to_dict() for rev in place.reviews]
    return jsonify(review_list)


@app_views.route('/reviews/<review_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def review_by_id(review_id):
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    if request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        try:
            request = request.get_json()
            request['created_at'] = review.created_at
            request['id'] = review.id
            try:
                request.pop('user_id', None)
                request.pop('place_id', None)
            except Exception as e:
                pass
            review = Review(**request)
            review.save()
            return jsonify(review.to_dict()), 200
        except Exception as e:
            abort(400, description='Not a JSON')
    return jsonify(review.to_dict())
