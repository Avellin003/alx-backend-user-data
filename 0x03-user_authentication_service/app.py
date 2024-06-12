#!/usr/bin/env python3
"""
Flask application
"""
from flask import (
    Flask,
    request,
    jsonify,
    abort,
    redirect,
    url_for
)

from auth import Auth

flask_app = Flask(__name__)
authentication = Auth()


@flask_app.route("/", methods=["GET"], strict_slashes=False)
def home() -> str:
    """
    Returns a JSON response
    {"message": "Bienvenue"}
    """
    return jsonify({"message": "Bienvenue"})


@flask_app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """
    Registers new users
    """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        user = authentication.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": f"{email}", "message": "user created"})


@flask_app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """
    Logs in a user if the credentials provided are correct, and create a new
    session for them.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not authentication.valid_login(email, password):
        abort(401)

    session_id = authentication.create_session(email)
    resp = jsonify({"email": f"{email}", "message": "logged in"})
    resp.set_cookie("session_id", session_id)
    return resp


@flask_app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """
    Logs out a logged in user and destroy their session
    """
    session_id = request.cookies.get("session_id", None)
    user = authentication.get_user_from_session_id(session_id)
    if user is None or session_id is None:
        abort(403)
    authentication.destroy_session(user.id)
    return redirect("/")


@flask_app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """
    Returns a user's email based on session_id in the received cookies
    """
    session_id = request.cookies.get("session_id")
    user = authentication.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": f"{user.email}"}), 200
    abort(403)


@flask_app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """
    Generates a token for resetting a user's password
    """
    email = request.form.get("email")
    try:
        reset_token = authentication.get_reset_password_token(email)
    except ValueError:
        abort(403)

    return jsonify({"email": f"{email}", "reset_token": f"{reset_token}"})


@flask_app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """
    Updates a user's password
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        authentication.update_password(reset_token, new_password)
    except ValueError:
        abort(403)

    return jsonify({"email": f"{email}", "message": "Password updated"})


if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port="5000")
