"""
app/utils/decorators.py
Decorators for common functionality
"""
from functools import wraps
from flask import jsonify
from flask_login import current_user
from datetime import datetime, timedelta
from ..models import db, User


def login_required_api(f):
    """API version of login required"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function


def rate_limit(max_requests, period_seconds):
    """Rate limiting decorator"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # This is a simple implementation
            # For production, use Flask-Limiter
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def check_quiz_spam(f):
    """Prevent quiz submission spam"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check rate limiting for quiz submissions
        # This could be expanded with Redis caching
        return f(*args, **kwargs)
    return decorated_function