import json
from flask import request, jsonify

def load_users():
    with open("users.json") as f:
        return json.load(f)

def authenticate(username, password):
    users = load_users()
    for user in users:
        if user["username"] == username and user["password"] == password:
            return user
    return None

def require_auth(f):
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return jsonify({"error": "Missing credentials"}), 401
        user = authenticate(auth.username, auth.password)
        if not user:
            return jsonify({"error": "Invalid credentials"}), 403
        request.user = user
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper
