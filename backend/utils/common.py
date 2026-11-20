# ReWear Clothing System - Common Utilities
# Helper functions for API responses and validation

import re
from datetime import datetime

def success_response(data, message='Success', status_code=200):
    """
    Create a success response
    """
    return {
        'success': True,
        'message': message,
        'data': data
    }, status_code


def error_response(message, status_code=400):
    """
    Create an error response
    """
    return {
        'success': False,
        'message': message,
        'data': None
    }, status_code


def validate_email(email):
    """
    Validate email format
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password):
    """
    Validate password strength
    Minimum 8 characters, at least one uppercase, one lowercase, one digit
    """
    if len(password) < 8:
        return False, 'Password must be at least 8 characters'
    
    if not re.search(r'[A-Z]', password):
        return False, 'Password must contain uppercase letter'
    
    if not re.search(r'[a-z]', password):
        return False, 'Password must contain lowercase letter'
    
    if not re.search(r'\d', password):
        return False, 'Password must contain digit'
    
    return True, 'Valid'


def sanitize_input(input_str):
    """
    Sanitize user input to prevent XSS
    """
    if not isinstance(input_str, str):
        return input_str
    
    # Remove HTML tags
    dangerous_chars = ['<', '>', '"', "'", '&']
    sanitized = input_str
    
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    
    return sanitized.strip()


def pagination_params(request):
    """
    Extract pagination parameters from request
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Validate pagination
    if page < 1:
        page = 1
    if per_page < 1 or per_page > 100:
        per_page = 10
    
    return page, per_page


def get_pagination_meta(queryset, page, per_page):
    """
    Build pagination metadata from MongoEngine queryset
    """
    total = queryset.count()
    total_pages = (total + per_page - 1) // per_page
    return {
        'total': total,
        'pages': total_pages,
        'current_page': page,
        'per_page': per_page,
        'has_next': page < total_pages,
        'has_prev': page > 1
    }
