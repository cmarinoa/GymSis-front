import json
from urllib import request, error


BASE_URL = "http://127.0.0.1:8000"


def send_post(endpoint, data, token=None):
    # Build the full URL and convert the Python dictionary into JSON
    url = BASE_URL + endpoint
    body = json.dumps(data).encode("utf-8")
    headers = {"Content-Type": "application/json"}

    if token:
        # Django uses this cookie to know which user is making the request
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
        # Even if the request fails, the backend usually returns a JSON error message
        return json.loads(e.read().decode("utf-8"))
    except error.URLError:
        return {"error": "Could not connect to the server"}


def send_get(endpoint, token=None):
    # GET requests do not send a body, only the URL and optional session cookie
    url = BASE_URL + endpoint
    headers = {}

    if token:
        # Reuse the login session so protected endpoints recognize the user
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
        # Return the backend error as a normal dictionary for the controller
        return json.loads(e.read().decode("utf-8"))
    except error.URLError:
        return {"error": "Could not connect to the server"}


# Register a new user in the backend
def register_user(name, password):
    # Sends the data entered in the register screen to the backend
    return send_post("/users/", {
        "name": name,
        "password": password
    })


# Log in an existing user in the backend
def login_user(name, password):
    # If login works, the backend returns a session token
    return send_post("/auth/login/", {
        "name": name,
        "password": password
    })


# Register a new gym session in the backend
def register_session(date, token):
    # Creates one session for the logged in user
    return send_post("/sessions/", {
        "date": date
    }, token)


# Get the logged in user's sessions
def get_sessions(token):
    # Loads every session that belongs to the logged in user
    return send_get("/sessions/", token)


# Register a new exercise in the backend
def register_exercise(exercise, token):
    # Sends either a cardio or weights exercise dictionary to the backend
    return send_post("/exercises/", exercise, token)


# Get the exercises from one session
def get_exercises(session_id, token):
    # Requests all exercises that belong to one session
    return send_get(f"/exercises/?session_id={session_id}", token)


# Register the user's body measurements
def register_measurements(measurements, token):
    # Saves the measurements from the profile screen
    return send_post("/profile/measurements/", measurements, token)


# Get the user's body measurements
def get_measurements(token):
    # Loads the latest saved measurements for the logged in user
    return send_get("/profile/measurements/", token)
