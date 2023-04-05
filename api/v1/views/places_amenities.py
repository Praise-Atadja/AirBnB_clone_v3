#!/usr/bin/python3
"""module"""

from models import storage
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', strict_slashes=False)
def get_amenities(place_id):
    """Retrieves the list of all Review objects of a Place """

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenities = place.amenities
    return jsonify([amenity.to_dict()
                    for amenity in amenities]), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_amenity(place_id, amenity_id):
    """ Deletes an Amenity object"""

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['POST'])
def link_amenity_to_place(place_id, amenity_id):
    """ Link Amenity object to place"""

    place = storage.get(Place, place_id)
    iif place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    place.amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201
