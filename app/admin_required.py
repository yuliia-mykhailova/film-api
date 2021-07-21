"""Module for admin_required decorator"""

from functools import wraps

from flask_login import current_user


def admin_required(func):
    """Check if user is admin decorator"""
    @wraps(func)
    def wrap(*args, **kwargs):
        if current_user.is_admin:
            return func(*args, **kwargs)
        return {"Error": "You don't have permission to do that"}, 403
    return wrap
