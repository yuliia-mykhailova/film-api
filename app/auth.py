"""Module for login manager"""

from app.models import User
from app import login_manager


@login_manager.user_loader
def load_user(user_id):
    """User loader"""
    return User.query.get(int(user_id))
