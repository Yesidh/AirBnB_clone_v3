#!/usr/bin/python3
"""
===========================================================
Retrieves the list of all Place objects of a City:
                                    GET /api/v1/cities/<city_id>/places
Retrieves a Place object. : GET /api/v1/places/<place_id>
Deletes a Place object: DELETE /api/v1/places/<place_id>
Creates a Place: POST /api/v1/cities/<city_id>/places
Updates a Place object: PUT /api/v1/places/<place_id>
===========================================================
"""

from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request, make_response
from models.place import Place


@app_views.route('/cities/<string:city_id>/places', strict_slashes=False)
def retrieve_places_from_city(city_id):
    """ Retrieves the list of all Place objects of a City"""

    place_list = []
    if storage.get("City", city_id) is not None:
        for place in storage.get("City", city_id).places:
            place_list.append(place.to_dict())
        return make_response(jsonify(place_list))
    else:
        return abort(404)


@app_views.route('/places/<string:place_id>', strict_slashes=False)
def place(place_id):
    """Method to retrieve Place"""

    if storage.get("Place", place_id) is not None:
        return jsonify(storage.get("Place", place_id).to_dict())
    else:
        abort(404)


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place_id(place_id):
    """Method to delete a Place object using the DELETE method and his id"""

    if storage.get("Place", place_id) is not None:
        obj = storage.get("Place", place_id)
        storage.delete(obj)
        storage.save()
        return make_response({}, 200)
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place_city(city_id):
    """Method to creates an Place object using POST"""

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if storage.get("City", city_id) is None:
        abort(404)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    if storage.get('User', request.get_json['user_id']) is not None:
        obj = request.get_json()
        obj['city_id'] = city_id
        new_obj = Place(**obj)
        storage.new(new_obj)
        storage.save()
        return make_response(new_obj.to_dict(), 201)
    else:
        abort(404)


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(place_id):
    """Method to update a Place object using PUT"""

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if storage.get("Place", place_id) is not None:
        obj = storage.get("Place", place_id)
        obj_dict = obj.to_dict()
        dict1 = request.get_json()
        ignored_keys = ['id', 'created_at', 'updated_at', 'user_id', 'city_id']
        for key, value in obj_dict.items():
            if key in ignored_keys:
                pass
            else:
                for k, v in dict1.items():
                    if key == k:
                        setattr(obj, k, v)
                    else:
                        pass
        obj.save()
        return make_response(obj.to_dict(), 200)
    else:
        abort(404)
