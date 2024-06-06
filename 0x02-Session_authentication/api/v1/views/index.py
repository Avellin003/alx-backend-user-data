#!/usr/bin/env python3
"""modules for the API"""
from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def authorized() -> str:
    """ GETS /api/v1/unauthorized
    returns:
        - the raise a 401 error
    """
    abort(401, description="Unauthorized")


@app_views.route('/forbidden', methods=['GET'], strict_slashes=False)
def forbid() -> str:
    """ GETS /api/v1/forbidden
    returns:
        - the raise a 403 error
    """
    abort(403, description="Forbidden")


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """ GETS /api/v1/status
    returns:
      - the status of the API and
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """ GETS /api/v1/stats
    returns:
      - the number of each objects by type
    """
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)
