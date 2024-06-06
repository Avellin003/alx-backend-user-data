#!/usr/bin/env python3
"""
This module sets up the routes for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os

# Initialize Flask app
app = Flask(__name__)
app.register_blueprint(app_views)
# Enable CORS
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
AUTHTYPE = os.getenv("AUTH_TYPE")
# Import the appropriate authentication class based on the AUTH_TYPE environment variable
if AUTHTYPE == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()
elif AUTHTYPE == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    aut = BasicAuth()
elif AUTHTYPE == "session_auth":
    from api.v1.auth.session_auth import SessionAuth
    aut = SessionAuth()
elif AUTHTYPE == "session_exp_auth":
    from api.v1.auth.session_exp_auth import SessionExpAuth
    aut = SessionExpAuth()
elif AUTHTYPE == "session_db_auth":
    from api.v1.auth.session_db_auth import SessionDBAuth
    aut = SessionDBAuth()

@app.before_request
def bef_req():
    """
    This function is run before each request. It checks if the request is authorized and aborts if not.
    """
    if aut is None:
        pass
    else:
        setattr(request, "current_user", aut.current_user(request))
        excluded = [
            '/api/v1/status/',
            '/api/v1/unauthorized/',
            '/api/v1/forbidden/',
            '/api/v1/auth_session/login/'
        ]
        if aut.require_auth(request.path, excluded):
            cookies = aut.session_cookie(request)
            if aut.authorization_header(request) is None and cookies is None:
                abort(401, description="Unauthorized")
            if aut.current_user(request) is None:
                abort(403, description="Forbidden")

@app.errorhandler(404)
def not_found(error) -> str:
    """ Handler for 404 errors. Returns a JSON response with an error message. """
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Handler for 401 errors. Returns a JSON response with an error message. """
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden(error) -> str:
    """ Handler for 403 errors. Returns a JSON response with an error message. """
    return jsonify({"error": "Forbidden"}), 403

if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    # Run the app
    app.run(host=host, port=port)
