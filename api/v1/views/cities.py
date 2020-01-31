#!/usr/bin/python3
"""
===========================================================
Retrieves the list of all City objects of a State:
                               GET /api/v1/states/<state_id>/cities
Retrieves a City object. : GET /api/v1/cities/<city_id>
Deletes a City object: DELETE /api/v1/cities/<city_id>
Creates a City: POST /api/v1/states/<state_id>/cities
Updates a City object: PUT /api/v1/cities/<city_id>
===========================================================
"""

from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request, make_response
from models.state import State
from models.state import City


@app_views.route('/states/<string:state_id>/cities', strict_slashes=False)
def retrieve_city_in_state(state_id):
    """ Retrieve the list of all City from an State objects"""

    city_list = []
    if storage.get("State", state_id) is not None:
        for city in storage.get("State", state_id).cities:
            city_list.append(city.to_dict())
        return make_response(jsonify(city_list))
    else:
        return abort(404)


@app_views.route('/cities/<string:city_id>', strict_slashes=False)
def city(city_id):
    """Method to retrieve City"""

    if storage.get("City", city_id) is not None:
        return jsonify(storage.get("City", city_id).to_dict())
    else:
        abort(404)


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_city_id(city_id):
    """Method to delete a City object using the DELETE method and his id"""

    if storage.get("City", city_id) is not None:
        obj = storage.get("City", city_id)
        storage.delete(obj)
        storage.save()
        return make_response({}, 200)
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_state_city(state_id):
    """Method to creates an City object using POST"""

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if storage.get("State", state_id) is None:
        abort(404)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    obj = request.get_json()
    obj['state_id'] = state_id
    new_obj = City(**obj)
    storage.new(new_obj)
    storage.save()
    return make_response(new_obj.to_dict(), 201)


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """Method to update a City object using PUT"""

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if storage.get("City", city_id) is not None:
        obj = storage.get("City", city_id)
        obj_dict = obj.to_dict()
        dict1 = request.get_json()
        ignored_keys = ['id', 'created_at', 'updated_at', 'state_id']
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
