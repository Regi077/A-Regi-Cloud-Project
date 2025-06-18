# =============================================================================
#  auth.py  --  Simple User Authentication & Auth Decorator for Cloud Compliance API
# =============================================================================
#  PURPOSE:
#   - Handles basic user authentication using credentials stored in users.json.
#   - Provides a decorator (require_auth) for protecting Flask API endpoints.
#
#  HOW IT WORKS:
#   - `authenticate`: Checks username/password against users.json.
#   - `require_auth`: Decorator that enforces authentication on protected endpoints.
#     - If credentials are missing/invalid, returns 401/403 and aborts request.
#     - On success, attaches user object to the Flask request for downstream use.
#
#  SECURITY NOTE:
#   - This is suitable for a development/demo environment.
#   - For production: use strong password hashing, token-based auth, and secure user storage.
#
#  Author: Reginald
#  Last updated: 18th June 2025
# =============================================================================

import json
from flask import request, jsonify

def load_users():
    """
    Load all user records from a local JSON file (users.json).
    Expected file format: list of dicts with 'username' and 'password' keys.
    Returns:
        List[Dict]: List of user records.
    """
    with open("users.json") as f:
        return json.load(f)

def authenticate(username, password):
    """
    Validate credentials against users.json.
    Returns user dict on success, else None.
    """
    users = load_users()
    for user in users:
        if user["username"] == username and user["password"] == password:
            return user
    return None

def require_auth(f):
    """
    Flask decorator to enforce HTTP Basic Auth on API endpoints.
    Usage:
        @require_auth
        def my_endpoint():
            ...
    Attaches user object to `request.user` if authentication succeeds.
    """
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return jsonify({"error": "Missing credentials"}), 401
        user = authenticate(auth.username, auth.password)
        if not user:
            return jsonify({"error": "Invalid credentials"}), 403
        request.user = user  # Attach user info to request object for downstream handlers
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

# =============================================================================
#  End of auth.py
# =============================================================================
