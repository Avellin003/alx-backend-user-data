#!/usr/bin/env python3
"""API module"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
aut = None
AUTHENTIC = os.getenv("AUTH_TYPE")
if AUTHENTIC == "auth":
    from api.v1.auth.auth import Auth
    aut = Auth()
elif AUTHENTIC == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    aut = BasicAuth()
elif AUTHENTIC == "session_auth":
    from api.v1.auth.session_auth import SessionAuth
    aut = SessionAuth()
elif AUTHENTIC == "session_exp_auth":
    from api.v1.auth.session_exp_auth import SessionExpAuth
    aut = SessionExpAuth()
elif AUTHENTIC == "session_db_auth":
    from api.v1.auth.session_db_auth import SessionDBAuth
    aut = SessionDBAuth()


@app.before_request
def bef_req():
    """Before request
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
    """ When no route is found
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """REQUESTS UNAUTHORIZED HANDLER
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ requests forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
