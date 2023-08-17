#!/usr/bin/env python3
"""
in this module we are going to be testing the functions
we have created so far
"""
import requests


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """
    here we wil test to see if this function
    registers a user to the database
    """
    data = {
            "email": email,
            "password": password
        }

    response = requests.post(
            "{}/users".format(BASE_URL),
            data=data
            )
    if response.status_code == 200:
        msg = {"email": email, "message": "user created"}
        assert response.json() == msg
    else:
        msg = {"message": "email already registered"}
        assert response.status_code == 400
        assert response.json() == msg


def log_in_wrong_password(email: str, password: str) -> None:
    """
    test if a user with a wrong password can log in
    """
    data = {
            "email": email,
            "password": password
        }
    response = requests.post(
            "{}/sessions".format(BASE_URL),
            data=data
        )
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    test to log a user in
    """
    data = {
            "email": email,
            "password": password
        }

    response = requests.post(
            "{}/sessions".format(BASE_URL),
            data=data
        )

    if response.status_code == 200:
        msg = {"email": email, "message": "logged in"}
        assert response.json() == msg
    else:
        assert response.status_code == 401

    session_id = response.cookies.get("session_id")

    return session_id


def profile_unlogged() -> None:
    """
    test to access a profile without logging in
    """
    cookies = {
            "session_id": ""
        }

    response = requests.get(
            "{}/profile".format(BASE_URL),
            cookies=cookies
        )

    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    test to acess a user profile while logged in
    """
    cookies = {
            "session_id": session_id
        }

    response = requests.get(
            "{}/profile".format(BASE_URL),
            cookies=cookies
        )

    msg = {"email": EMAIL}
    assert response.status_code == 200
    assert response.json() == msg


def log_out(session_id: str) -> None:
    """
    log out user from a session
    """
    cookies = {
            "session_id": session_id
        }

    response = requests.delete(
            "{}/sessions".format(BASE_URL),
            cookies=cookies
        )

    if response.status_code == 302:
        msg = {"message": "Bienvenue"}
        assert response.json() == msg
    else:
        assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """
    test to set up a reset token for a user
    """
    data = {
            "email": email
        }

    response = requests.post(
            "{}/reset_password".format(BASE_URL),
            data=data
        )

    if response.status_code == 200:
        reset_token = response.json().get("reset_token")
        msg = {"email": email, "reset_token": reset_token}
        assert response.json() == msg

        return reset_token
    else:
        assert response.status_code == 403


def update_password(email: str, reset_token: str, new_password) -> None:
    """
    test to see if api really uodates a password
    """
    data = {
            "email": email,
            "reset_token": reset_token,
            "new_password": new_password
        }

    response = requests.put(
            "{}/reset_password".format(BASE_URL),
            data=data
        )

    if response.status_code == 200:
        msg = {"email": email, "message": "Password updated"}
        assert response.json() == msg
    else:
        assert response.status_code == 403


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
