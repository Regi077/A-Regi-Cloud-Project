# =============================================================================
#  rbac.py  --  Role-Based Access Control Decorator for Cloud Compliance API
# =============================================================================
#  Author: Reginald
#  Last updated: 18th June 2025
#
#  PURPOSE:
#    - Enforce fine-grained, role-based access control (RBAC) for Flask endpoints.
#    - Restrict sensitive operations (like uploads, scans) to only authorized user roles.
#
#  USAGE:
#    @require_role("admin", "Service Provider")
#    def upload_doc(): ...
#
#  HOW IT WORKS:
#    - The decorator checks that the authenticated user (attached to the Flask request)
#      matches at least one of the allowed roles.
#    - If the user is missing, or the role does not match, returns HTTP 403 Forbidden.
#    - Roles must match exactly, including case (e.g., "Service Provider").
# =============================================================================

from flask import request

def require_role(*roles):
    """
    Flask decorator for restricting endpoint access to one or more roles.
    Usage:
        @require_role("admin", "Service Provider")
        def endpoint(...):
            ...
    """
    def decorator(f):
        def wrapper(*args, **kwargs):
            # User must be set on request (by prior authentication middleware)
            user = getattr(request, 'user', None)
            if not user or user["role"] not in roles:
                # If user not present or role not allowed, return HTTP 403
                return {"error": "Forbidden"}, 403
            # Otherwise, proceed to actual endpoint handler
            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator

# =============================================================================
#  End of rbac.py  (Ensures all sensitive API endpoints are properly role-protected)
# =============================================================================
