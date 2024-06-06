#!/usr/bin/env python3
""" This module contains the views for the index routes """
from flask import jsonify, abort
from api.v1.views import app_views

@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def authorized() -> str:
    """ 
    Route: GET /api/v1/unauthorized
    Description: Raises a 401 error
    """
    abort(401, description="Unauthorized")

@app_views.route('/forbidden', methods=['GET'], strict_slashes=False)
def forbid() -> str:
    """ 
    Route: GET /api/v1/forbidden
    Description: Raises a 403 error
    """
    abort(403, description="Forbidden")

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """ 
    Route: GET /api/v1/status
    Description: Returns the status of the API
    """
    return jsonify({"status": "OK"})

@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """ 
    Route: GET /api/v1/stats
    Description: Returns the count of each object type
    """
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)
