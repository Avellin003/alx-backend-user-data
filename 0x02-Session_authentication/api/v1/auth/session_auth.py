#!/usr/bin/env python3
"""Session Auth module"""
import os
from flask import jsonify, request
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session():
    """
    Deals with user login
    retuns:
        the dict representation of user if found else error message
    """
    emails = request.form.get('email')
    passwords = request.form.get('password')
    if emails is None or emails == '':
        return jsonify({"error": "email missing"}), 400
    if passwords is None or passwords == '':
        return jsonify({"error": "password missing"}), 400
    users = User.search({"email": emails})
    if not users or users == []:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if user.is_valid_password(passwords):
            from api.v1.app import aut
            session_id = aut.create_session(user.id)
            respond = jsonify(user.to_json())
            session_name = os.getenv('SESSION_NAME')
            respond.set_cookie(session_name, session_id)
            return respond
    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def handle_logout():
    """deals with user logout
    """
    from api.v1.app import aut
    if aut.destroy_session(request):
        return jsonify({}), 200
    abort(404)
