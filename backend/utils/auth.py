# ReWear Clothing System - Authentication Utilities
# JWT and authorization helper functions

from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from models.models import User

def token_required(f):
    """
    Decorator to require valid JWT token in request
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'message': 'Unauthorized access'}), 401
    return decorated


def admin_required(f):
    """
    Decorator to require admin role
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = User.objects(id=user_id).first()
            
            if not user or user.role != 'admin':
                return jsonify({'message': 'Admin access required'}), 403
            
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'message': 'Unauthorized access'}), 401
    return decorated


def get_current_user():
    """
    Get current authenticated user
    """
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        return User.objects(id=user_id).first()
    except:
        return None


def validate_user_id(f):
    """
    Decorator to validate user ID in request
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            
            # Check if user exists
            user = User.objects(id=user_id).first()
            if not user:
                return jsonify({'message': 'User not found'}), 404
            
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'message': 'Invalid request'}), 400
    return decorated
