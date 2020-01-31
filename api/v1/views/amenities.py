#!/usr/bin/python3
"""
===========================================================
Retrieve the list of all State objects: GET /api/v1/states
Retrieve a State object: GET /api/v1/states/<state_id>
Delete State object: DELETE /api/v1/staes/<state_id>
Creates a State: POST /api/v1/states
Updates a State: PUT /api/v1/states/<state_id>
===========================================================
"""

from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request, make_response
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def retrieve_amenities():
    """ Retrieve the list of all Amenity objects"""

    amenity_list = []
    for key, value in storage.all("Amenity").items():
        amenity_list.append(value.to_dict())
    return jsonify(amenity_list)


@app_views.route('/amenities/<string:amenity_id>', strict_slashes=False,
                 methods=['GET'])
def amenities_id(amenity_id):
    """Method to retrieve an state using the id"""

    key = 'Amenity.' + amenity_id
    if key in storage.all("Amenity").keys():
        return jsonify(storage.all("Amenity").get(key).to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_amenities_id(amenity_id):
    """Method to delete an state object using the DELETE method and his id"""

    key = 'Amenity.' + amenity_id
    if key in storage.all("Amenity").keys():
        obj = storage.get("Amenity", amenity_id)
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/amenities/', methods=['POST'], strict_slashes=False)
def post_amenity():
    """Method to creates an State object using POST"""

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    obj = Amenity(**request.get_json())
    obj.save()
    return make_response(obj.to_dict(), 201)


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """Method to update an State object using PUT"""

    key = 'Amenity.' + amenity_id
    if key not in storage.all("Amenity").keys():
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get("Amenity", amenity_id)
    obj_dict = storage.all("Amenity").get(key).to_dict()
    ignored_keys = ['id', 'created_at', 'updated_at']
    obj2_dict = request.get_json()
    for key, value in obj_dict.items():
        if key in ignored_keys:
            pass
        else:
            for k, v in obj2_dict.items():
                if key == k:
                    setattr(obj, k, v)
                else:
                    pass
    obj.save()
    return make_response(obj.to_dict(), 200)
