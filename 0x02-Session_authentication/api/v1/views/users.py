#!/usr/bin/env python3
""" User routes views module """
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """ 
    GET /api/v1/users
    Return: JSON list of all User objects
    """
    allu = [user.to_json() for user in User.all()]
    return jsonify(allu)

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """ 
    GET /api/v1/users/:id
    Return: JSON of a User object or 404 if the User ID doesn't exist
    """
    if user_id is None:
        abort(404)
    if user_id == "me":
        if request.current_user is None:
            abort(404)
        user = request.current_user
        return jsonify(user.to_json())
    user = User.get(user_id)
    if user is None:
        abort(404)
    if request.current_user is None:
        abort(404)
    return jsonify(user.to_json())

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """ 
    DELETE /api/v1/users/:id
    Return: Empty JSON if the User has been deleted or 404 if the User ID doesn't exist
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    user.remove()
    return jsonify({}), 200

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """ 
    POST /api/v1/users/
    Return: JSON of the created User object or 400 if the User cannot be created
    """
    rjs = None
    error_sms = None
    try:
        rjs = request.get_json()
    except Exception as e:
        rjs = None
    if rjs is None:
        error_sms = "Wrong format"
    if error_sms is None and rjs.get("email", "") == "":
        error_sms = "email missing"
    if error_sms is None and rjs.get("password", "") == "":
        error_sms = "password missing"
    if error_sms is None:
        try:
            user = User()
            user.emails = rjs.get("email")
            user.password = rjs.get("password")
            user.first_name = rjs.get("first_name")
            user.last_name = rjs.get("last_name")
            user.save()
            return jsonify(user.to_json()), 201
        except Exception as e:
            error_msg = "Can't create User: {}".format(e)
    return jsonify({'error': error_msg}), 400

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """ 
    PUT /api/v1/users/:id
    Return: JSON of the updated User object or 404 if the User ID doesn't exist or 400 if the User cannot be updated
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    rjs = None
    try:
        rjs = request.get_json()
    except Exception as e:
        rjs = None
    if rjs is None:
        return jsonify({'error': "Wrong format"}), 400
    if rjs.get('first_name') is not None:
        user.first_name = rjs.get('first_name')
    if rjs.get('last_name') is not None:
        user.last_name = rjs.get('last_name')
    user.save()
    return jsonify(user.to_json()), 200
