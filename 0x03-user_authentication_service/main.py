#!/usr/bin/env python3
"""
Primary script
"""
import requests


def register_user(email: str, password: str) -> None:
    """
    Function to register a user with provided email and password.
    Args:
        email: User's email.
        password: User's password.
    Returns:
        None
    """
    response = requests.post('http://127.0.0.1:5000/users',
                             data={'email': email, 'password': password})
    if response.status_code == 200:
        assert (response.json() == {"email": email, "message": "user created"})
    else:
        assert(response.status_code == 400)
        assert (response.json() == {"message": "email already registered"})


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Function to test login with incorrect credentials.
    Args:
        email: User's email.
        password: User's password.
    Returns:
        None
    """
    res = requests.post('http://127.0.0.1:5000/sessions',
                        data={'email': email, 'password': password})
    assert (res.status_code == 401)


def profile_unlogged() -> None:
    """
    Function to test profile access without login.
    Returns:
        None
    """
    res = requests.get('http://127.0.0.1:5000/profile')
    assert(res.status_code == 403)


def log_in(email: str, password: str) -> str:
    """
    Function to test login with correct credentials.
    Args:
        email: User's email.
        password: User's password.
    Returns:
        User's session_id.
    """
    response = requests.post('http://127.0.0.1:5000/sessions',
                             data={'email': email, 'password': password})
    assert (response.status_code == 200)
    assert(response.json() == {"email": email, "message": "logged in"})
    return response.cookies['session_id']


def profile_logged(session_id: str) -> None:
    """
    Function to test profile access with login.
    Args:
        session_id: User's session_id.
    Returns:
        None
    """
    cookie_data = {'session_id': session_id}
    res = requests.get('http://127.0.0.1:5000/profile',
                       cookies=cookie_data)
    assert(res.status_code == 200)


def log_out(session_id: str) -> None:
    """
    Function to test logout.
    Args:
        session_id: User's session_id.
    Returns:
        None
    """
    cookie_data = {'session_id': session_id}
    res = requests.delete('http://127.0.0.1:5000/sessions',
                          cookies=cookie_data)
    if res.status_code == 302:
        assert(res.url == 'http://127.0.0.1:5000/')
    else:
        assert(res.status_code == 200)


def reset_password_token(email: str) -> str:
    """
    Function to test password reset token generation.
    Args:
        email: User's email.
    Returns:
        User's reset_token.
    """
    res = requests.post('http://127.0.0.1:5000/reset_password',
                        data={'email': email})
    if res.status_code == 200:
        return res.json()['reset_token']
    assert(res.status_code == 401)


def update_password(email: str, reset_token: str,
                    new_password: str) -> None:
    """
    Function to test password update.
    Args:
        email: User's email.
        reset_token: User's reset_token.
        new_password: User's new password.
    Returns:
        None
    """
    data = {'email': email, 'reset_token': reset_token,
            'new_password': new_password}
    res = requests.put('http://127.0.0.1:5000/reset_password',
                       data=data)
    if res.status_code == 200:
        assert(res.json() == {"email": email, "message": "Password updated"})
    else:
        assert(res.status_code == 403)


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
