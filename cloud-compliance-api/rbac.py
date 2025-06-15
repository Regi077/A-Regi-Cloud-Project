from flask import request

def require_role(*roles):
    def decorator(f):
        def wrapper(*args, **kwargs):
            user = getattr(request, 'user', None)
            if not user or user["role"] not in roles:
                return {"error": "Forbidden"}, 403
            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator
