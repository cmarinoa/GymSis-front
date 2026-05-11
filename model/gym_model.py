import json
import os
from urllib import request, error


BASE_URL = "http://127.0.0.1:8000"
SESSION_FILE = os.path.join(os.path.dirname(__file__), "saved_session.json")


def send_request(method, endpoint, data=None, token=None):
    # Build the full URL and prepare the common headers
    url = BASE_URL + endpoint
    headers = {}

    if data is not None:
        headers["Content-Type"] = "application/json"

    if token:
        # Django uses this cookie to know which user is making the request
        headers["Cookie"] = "sessionid=" + token

    body = None

    if data is not None:
        # Convert the Python dictionary into JSON only when needed
        body = json.dumps(data).encode("utf-8")

    req = request.Request(
        url,
        data=body,
        headers=headers,
        method=method
    )

    try:
        response = request.urlopen(req)
        return json.loads(response.read().decode("utf-8"))
    except error.HTTPError as e:
        # Return the backend error as a normal dictionary for the controller
        return json.loads(e.read().decode("utf-8"))
    except error.URLError:
        return {"error": "Could not connect to the server"}


def send_post(endpoint, data, token=None):
    return send_request("POST", endpoint, data, token)


def send_get(endpoint, token=None):
    return send_request("GET", endpoint, token=token)


def send_put(endpoint, data, token=None):
    return send_request("PUT", endpoint, data, token)


def send_delete(endpoint, token=None):
    return send_request("DELETE", endpoint, token=token)


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


# Check if the saved token still belongs to a valid session
def get_saved_session(token):
    # This is used when the app opens to avoid asking the user to log in again
    return send_get("/auth/session/", token)


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
    return send_post("/profile/", measurements, token)


# Get the user's body measurements
def get_measurements(token):
    # Loads the latest saved measurements for the logged in user
    return send_get("/profile/", token)


# Update one session in the backend
def update_session(session_id, date, token):
    return send_put(f"/sessions/{session_id}/", {
        "date": date
    }, token)


# Delete one session in the backend
def delete_session(session_id, token):
    return send_delete(f"/sessions/{session_id}/", token)


# Update one exercise in the backend
def update_exercise(exercise_id, exercise, token):
    return send_put(f"/exercises/{exercise_id}/", exercise, token)


# Delete one exercise in the backend
def delete_exercise(exercise_id, token):
    return send_delete(f"/exercises/{exercise_id}/", token)


# Save the current session token in a local file
def save_session_token(token):
    # The desktop app reads this file when it starts again
    with open(SESSION_FILE, "w", encoding="utf-8") as session_file:
        json.dump({"token": token}, session_file)


# Load the saved session token from the local file
def load_session_token():
    if not os.path.exists(SESSION_FILE):
        return None

    try:
        with open(SESSION_FILE, "r", encoding="utf-8") as session_file:
            data = json.load(session_file)
    except (OSError, json.JSONDecodeError):
        return None

    return data.get("token")


# Delete the saved token when the user logs out
def clear_session_token():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
