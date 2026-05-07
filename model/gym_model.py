import json
from urllib import request, error


BASE_URL = "http://127.0.0.1:8000"


def send_post(endpoint, data, token=None):
    url = BASE_URL + endpoint
    body = json.dumps(data).encode("utf-8")
    headers = {"Content-Type": "application/json"}

    if token:
        headers["Cookie"] = "sessionid=" + token

    req = request.Request(
        url,
        data=body,
        headers=headers,
        method="POST"
    )

    try:
        response = request.urlopen(req)
        return json.loads(response.read().decode("utf-8"))
    except error.HTTPError as e:
        return json.loads(e.read().decode("utf-8"))
    except error.URLError:
        return {"error": "Could not connect to the server"}


def send_get(endpoint, token=None):
    url = BASE_URL + endpoint
    headers = {}

    if token:
        headers["Cookie"] = "sessionid=" + token

    req = request.Request(
        url,
        headers=headers,
        method="GET"
    )

    try:
        response = request.urlopen(req)
        return json.loads(response.read().decode("utf-8"))
    except error.HTTPError as e:
        return json.loads(e.read().decode("utf-8"))
    except error.URLError:
        return {"error": "Could not connect to the server"}


# Register a new user in the backend
def register_user(name, password):
    return send_post("/users/", {
        "name": name,
        "password": password
    })


# Log in an existing user in the backend
def login_user(name, password):
    return send_post("/auth/login/", {
        "name": name,
        "password": password
    })


# Register a new gym session in the backend
def register_session(date, token):
    return send_post("/sessions/", {
        "date": date
    }, token)


# Get the logged in user's sessions
def get_sessions(token):
    return send_get("/sessions/", token)


# Register a new exercise in the backend
def register_exercise(exercise, token):
    return send_post("/exercises/", exercise, token)


# Get the exercises from one session
def get_exercises(session_id, token):
    return send_get(f"/exercises/?session_id={session_id}", token)


# Register the user's body measurements
def register_measurements(measurements, token):
    return send_post("/profile/measurements/", measurements, token)


# Get the user's body measurements
def get_measurements(token):
    return send_get("/profile/measurements/", token)
