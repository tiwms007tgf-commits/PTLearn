"""
app/utils/validators.py
Input validation utilities
"""
import re
from email_validator import validate_email as email_validate, EmailNotValidError


def validate_username(username):
    """Validate username format"""
    if not username:
        return False
    
    if len(username) < 3 or len(username) > 20:
        return False
    
    # Only alphanumeric and underscore
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False
    
    return True


def validate_email(email):
    """Validate email format"""
    try:
        email_validate(email)
        return True
    except EmailNotValidError:
        return False


def validate_password(password):
    """Validate password strength"""
    if not password:
        return False
    
    if len(password) < 8:
        return False
    
    return True


def validate_code(code):
    """Validate Python code"""
    if not code:
        return False
    
    if len(code) > 10000:
        return False
    
    return True


def sanitize_input(data):
    """Sanitize user input"""
    if isinstance(data, str):
        return data.strip()[:1000]  # Max 1000 chars
    
    return data