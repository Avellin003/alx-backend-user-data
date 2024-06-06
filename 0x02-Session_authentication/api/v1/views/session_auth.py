#!/usr/bin/env python3
""" This module contains the views for User routes """
import os
from flask import jsonify, request
from api.v1.views import app_views
from models.user import User

@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session():
    """
    Route: POST /auth_session/login
    Description: Handles user login. Returns a JSON representation of the user if found, else returns an error message.
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
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            resp = jsonify(user.to_json())
            session_name = os.getenv('SESSION_NAME')
            resp.set_cookie(session_name, session_id)
            return resp
    return jsonify({"error": "wrong password"}), 401

@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def handle_logout():
    """
    Route: DELETE /auth_session/logout
    Description: Handles user logout. Destroys the session if it exists.
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
