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
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def retrieve_users():
    """ Retrieve the list of all User objects"""

    user_list = []
    for key, value in storage.all("User").items():
        user_list.append(value.to_dict())
    return jsonify(user_list)


@app_views.route('/users/<string:user_id>', strict_slashes=False,
                 methods=['GET'])
def users_id(user_id):
    """Method to retrieve an user using the id"""

    key = 'User.' + user_id
    if key in storage.all("User").keys():
        return jsonify(storage.all("User").get(key).to_dict())
    else:
        abort(404)


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_users_id(user_id):
    """Method to delete an user object using the DELETE method and his id"""

    key = 'User.' + user_id
    if key in storage.all("User").keys():
        obj = storage.get("User", user_id)
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/users/', methods=['POST'], strict_slashes=False)
def post_user():
    """Method to creates an User object using POST"""

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    if 'email' not in request.get_json():
        return make_response(jsonify({"error": "Missing email"}), 400)
    if 'password' not in request.get_json():
        return make_response(jsonify({"error": "Missing password"}), 400)
    obj = User(**request.get_json())
    obj.save()
    return make_response(obj.to_dict(), 201)


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """Method to update an User object using PUT"""

    key = 'User.' + user_id
    if key not in storage.all("User").keys():
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get("User", amenity_id)
    obj_dict = storage.all("User").get(key).to_dict()
    ignored_keys = ['id', 'email', 'created_at', 'updated_at']
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
