#!/usr/bin/python3
"""
Creates a new view for Place objects that handles all default RESTFul API actions
"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False)
def users():
    """Retrieves the list of all User objects"""
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@app_views.route('/users/<user_id>', strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict()), 200


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def add_user():
    """Creates a User"""
    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    if 'email' not in data:
        abort(400, description="Missing email")
    if 'password' not in data:
        abort(400, description="Missing password")
    user = User(**data)
    user.save()

    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """Updates a User object"""
    if not request.is_json:
        abort(400, description="Not a JSON")
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
