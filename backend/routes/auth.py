# ReWear Clothing System - Authentication Routes
# User registration, login, and token management endpoints

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from database import db
from models.models import User
from utils.common import success_response, error_response, validate_email, validate_password, sanitize_input
from utils.auth import token_required

auth_bp = Blueprint('auth', __name__)

# ============================================
# USER REGISTRATION
# ============================================
@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user

    Request JSON:
    {
        "username": "string",
        "email": "string",
        "password": "string",
        "full_name": "string",
        "mobile": "string (optional)",
        "address": "string (optional)"
    }
    """
    try:
        data = request.get_json()

        # Validate required fields
        if not data or not all(k in data for k in ['username', 'email', 'password', 'full_name']):
            return error_response('Missing required fields', 400)

        # Sanitize inputs
        username = sanitize_input(data['username'])
        email = sanitize_input(data['email'])
        full_name = sanitize_input(data['full_name'])

        # Validate email
        if not validate_email(email):
            return error_response('Invalid email format', 400)

        # Validate password
        valid_password, password_msg = validate_password(data['password'])
        if not valid_password:
            return error_response(password_msg, 400)

        # Check if user already exists
        if User.objects(username=username).first():
            return error_response('Username already exists', 409)

        if User.objects(email=email).first():
            return error_response('Email already registered', 409)

        # Create new user
        user = User(
            username=username,
            email=email,
            full_name=full_name,
            mobile=data.get('mobile', ''),
            address=data.get('address', ''),
            role='user'
        )

        # Set password
        user.set_password(data['password'])

        # Save to MongoDB
        user.save()

        return success_response({
            'user_id': str(user.id),
            'username': user.username,
            'email': user.email
        }, 'User registered successfully', 201)

    except Exception as e:
        return error_response(f'Registration failed: {str(e)}', 500)


# ============================================
# USER LOGIN
# ============================================
@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User login - returns JWT tokens
    
    Request JSON:
    {
        "email": "string",
        "password": "string"
    }
    """
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ['email', 'password']):
            return error_response('Email and password required', 400)
        
        email = sanitize_input(data['email'])
        
        # Find user by email
        user = User.objects(email=email).first()
        
        if not user or not user.check_password(data['password']):
            return error_response('Invalid email or password', 401)
        
        if not user.is_active:
            return error_response('Account is disabled', 403)
        
        # Generate JWT tokens
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        
        return success_response({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        }, 'Login successful', 200)
    
    except Exception as e:
        return error_response(f'Login failed: {str(e)}', 500)


# ============================================
# REFRESH TOKEN
# ============================================
@auth_bp.route('/refresh-token', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    """
    Refresh access token using refresh token
    """
    try:
        user_id = get_jwt_identity()
        user = User.objects(id=user_id).first()
        
        if not user or not user.is_active:
            return error_response('Invalid refresh token', 401)
        
        # Generate new access token
        access_token = create_access_token(identity=str(user.id))
        
        return success_response({
            'access_token': access_token,
            'token_type': 'Bearer'
        }, 'Token refreshed', 200)
    
    except Exception as e:
        return error_response(f'Token refresh failed: {str(e)}', 500)


# ============================================
# USER LOGOUT (Optional - typically handled on client)
# ============================================
@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout():
    """
    User logout
    Note: JWTs are stateless, so logout is handled on client-side by discarding tokens
    """
    return success_response({}, 'Logout successful', 200)


# ============================================
# PASSWORD RESET REQUEST
# ============================================
@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    """
    Request password reset - in production, send email with reset token
    
    Request JSON:
    {
        "email": "string"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'email' not in data:
            return error_response('Email required', 400)
        
        email = sanitize_input(data['email'])
        user = User.objects(email=email).first()
        
        # Don't reveal if user exists (security best practice)
        if user:
            # In production: generate reset token, save to database, send via email
            # For now, just acknowledge the request
            pass
        
        return success_response({}, 'If user exists, password reset email has been sent', 200)
    
    except Exception as e:
        return error_response(f'Password reset failed: {str(e)}', 500)


# ============================================
# VERIFY EMAIL
# ============================================
@auth_bp.route('/verify-email', methods=['POST'])
def verify_email():
    """
    Verify email (typically via link in email)
    
    Request JSON:
    {
        "token": "string"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'token' not in data:
            return error_response('Verification token required', 400)
        
        # In production: verify token, mark user email as verified
        
        return success_response({}, 'Email verified successfully', 200)
    
    except Exception as e:
        return error_response(f'Email verification failed: {str(e)}', 500)
