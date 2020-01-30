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
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def retrieve_states():
    """ Retrieve the list of all State objects"""

    state_list = []
    for key, value in storage.all("State").items():
        state_list.append(value.to_dict())
    return jsonify(state_list)


@app_views.route('/states/<string:state_id>', strict_slashes=False,
                 methods=['GET'])
def states_id(state_id):
    """Method to retrieve an state using the id"""

    key = 'State.' + state_id
    if key in storage.all("State").keys():
        return jsonify(storage.all("State").get(key).to_dict())
    else:
        abort(404)


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_states_id(state_id):
    """Method to delete an state object using the DELETE method and his id"""

    key = 'State.' + state_id
    if key in storage.all("State").keys():
        obj = storage.get("State", state_id)
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def post_state():
    """Method to creates an State object using POST"""

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    obj = State(**request.get_json())
    obj.save()
    return make_response(obj.to_dict(), 201)


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_state(state_id):
    """Method to update an State object using PUT"""

    key = 'State.' + state_id
    if key not in storage.all("State").keys():
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.all("State").get(key).to_dict()
    ignored_keys = ['id', 'created_at', 'updated_at']
    obj2 = request.get_json()
    for key, value in obj.items():
        if key in ignored_keys:
            pass
        else:
            for k, v in obj2.items():
                if key == k:
                    obj[key] = v
                'else:
                    pass'
    storage.save()
    return make_response(obj, 200)
