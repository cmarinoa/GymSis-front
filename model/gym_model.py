import json
from urllib import request, error


BASE_URL = "http://127.0.0.1:8000"


def send_post(endpoint, data):
    url = BASE_URL + endpoint
    body = json.dumps(data).encode("utf-8")

    req = request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST"
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
    return send_post("/register/", {
        "name": name,
        "password": password
    })


# Log in an existing user in the backend
def login_user(name, password):
    return send_post("/login/", {
        "name": name,
        "password": password
    })
