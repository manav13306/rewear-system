# ReWear Clothing System - User Routes
# User profile management endpoints

from flask import Blueprint, request, jsonify
from mongoengine.errors import OperationError
from models.models import User, ImpactMetrics
from utils.common import success_response, error_response, sanitize_input, pagination_params
from utils.auth import token_required, admin_required, get_current_user
from utils.sustainability import ImpactReport
from flask_jwt_extended import get_jwt_identity

users_bp = Blueprint('users', __name__)

# ============================================
# GET CURRENT USER PROFILE
# ============================================
@users_bp.route('/me', methods=['GET'])
@token_required
def get_current_user_profile():
    """
    Get current authenticated user's profile
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.objects(id=current_user_id).first()
        
        if not user:
            return error_response('User not found', 404)
        
        return success_response(user.to_dict(), 'Current user retrieved', 200)
    
    except Exception as e:
        return error_response(f'Error retrieving current user: {str(e)}', 500)


# ============================================
# SEARCH USERS (Admin only)
# ============================================
@users_bp.route('/search', methods=['GET'])
@admin_required
def search_users():
    """
    Search users by username or email (admin only)
    """
    try:
        query_str = request.args.get('q', '', type=str)
        
        if not query_str or len(query_str) < 2:
            return error_response('Search query too short (minimum 2 characters)', 400)
        
        page, per_page = pagination_params(request)
        
        # MongoDB regex search
        query = User.objects(
            __raw__={
                '$or': [
                    {'username': {'$regex': query_str, '$options': 'i'}},
                    {'email': {'$regex': query_str, '$options': 'i'}},
                    {'full_name': {'$regex': query_str, '$options': 'i'}}
                ]
            }
        )
        total = query.count()
        users = query.skip((page-1)*per_page).limit(per_page)
        
        total_pages = (total + per_page - 1) // per_page
        
        return success_response({
            'users': [user.to_dict() for user in users],
            'pagination': {
                'total': total,
                'pages': total_pages,
                'current_page': page,
                'per_page': per_page,
                'has_next': page < total_pages,
                'has_prev': page > 1
            }
        }, 'Search completed', 200)
    
    except Exception as e:
        return error_response(f'Error searching users: {str(e)}', 500)


# ============================================
# LIST ALL USERS (Admin only)
# ============================================
@users_bp.route('', methods=['GET'])
@admin_required
def list_users():
    """
    List all users (admin only)
    """
    try:
        page, per_page = pagination_params(request)
        
        query = User.objects()
        total = query.count()
        users = query.skip((page-1)*per_page).limit(per_page)
        
        total_pages = (total + per_page - 1) // per_page
        
        return success_response({
            'users': [user.to_dict() for user in users],
            'pagination': {
                'total': total,
                'pages': total_pages,
                'current_page': page,
                'per_page': per_page,
                'has_next': page < total_pages,
                'has_prev': page > 1
            }
        }, 'Users retrieved successfully', 200)
    
    except Exception as e:
        return error_response(f'Error retrieving users: {str(e)}', 500)


# ============================================
# GET USER PROFILE
# ============================================
@users_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    """
    Get user profile information
    """
    try:
        user = User.objects(id=user_id).first()
        
        if not user:
            return error_response('User not found', 404)
        
        return success_response(user.to_dict(), 'User retrieved successfully', 200)
    
    except Exception as e:
        return error_response(f'Error retrieving user: {str(e)}', 500)


# ============================================
# UPDATE USER PROFILE
# ============================================
@users_bp.route('/<user_id>', methods=['PUT'])
@token_required
def update_user(user_id):
    """
    Update user profile (only own profile or admin)
    
    Request JSON:
    {
        "full_name": "string",
        "mobile": "string",
        "address": "string",
        "bio": "string",
        "profile_image_url": "string"
    }
    """
    try:
        current_user_id = get_jwt_identity()
        
        # Allow users to update only their own profile or admins to update any
        user = User.objects(id=user_id).first()
        if not user:
            return error_response('User not found', 404)
        
        # Permission check
        if str(current_user_id) != str(user_id):
            current_user = User.objects(id=current_user_id).first()
            if not current_user or current_user.role != 'admin':
                return error_response('Permission denied', 403)
        
        data = request.get_json() or {}
        
        # Update allowed fields
        if 'full_name' in data:
            user.full_name = sanitize_input(data['full_name'])
        if 'mobile' in data:
            user.mobile = sanitize_input(data['mobile'])
        if 'address' in data:
            user.address = sanitize_input(data['address'])
        if 'bio' in data:
            user.bio = sanitize_input(data['bio'])
        if 'profile_image_url' in data:
            user.profile_image_url = sanitize_input(data['profile_image_url'])
        
        user.save()
        
        return success_response(user.to_dict(), 'User updated successfully', 200)
    
    except Exception as e:
        return error_response(f'Error updating user: {str(e)}', 500)


# ============================================
# GET USER SUSTAINABILITY IMPACT
# ============================================
@users_bp.route('/<user_id>/impact', methods=['GET'])
def get_user_impact(user_id):
    """
    Get user's sustainability impact summary
    """
    try:
        user = User.objects(id=user_id).first()
        
        if not user:
            return error_response('User not found', 404)
        
        impact_summary = ImpactReport.get_user_impact_summary(user)
        
        return success_response(impact_summary, 'Impact summary retrieved', 200)
    
    except Exception as e:
        return error_response(f'Error retrieving impact: {str(e)}', 500)


# ============================================
# GET USER IMPACT HISTORY
# ============================================
@users_bp.route('/<user_id>/impact-history', methods=['GET'])
def get_user_impact_history(user_id):
    """
    Get detailed impact history for a user
    """
    try:
        user = User.objects(id=user_id).first()
        if not user:
            return error_response('User not found', 404)
        
        page, per_page = pagination_params(request)
        
        query = ImpactMetrics.objects(user=user).order_by('-created_at')
        total = query.count()
        impacts = query.skip((page-1)*per_page).limit(per_page)
        
        total_pages = (total + per_page - 1) // per_page
        
        return success_response({
            'impacts': [impact.to_dict() for impact in impacts],
            'pagination': {
                'total': total,
                'pages': total_pages,
                'current_page': page,
                'per_page': per_page,
                'has_next': page < total_pages,
                'has_prev': page > 1
            }
        }, 'Impact history retrieved', 200)
    
    except Exception as e:
        return error_response(f'Error retrieving impact history: {str(e)}', 500)


# ============================================
# DELETE USER (Admin only)
# ============================================
@users_bp.route('/<user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    """
    Delete user (admin only)
    """
    try:
        user = User.objects(id=user_id).first()
        
        if not user:
            return error_response('User not found', 404)
        
        try:
            user.delete()
            return success_response({}, 'User deleted successfully', 200)
        except OperationError:
            # Preserve referential integrity for existing transactions.
            user.is_active = False
            user.save()
            return success_response(
                user.to_dict(),
                'User has related records and was deactivated instead of deleted',
                200
            )
    
    except Exception as e:
        return error_response(f'Error deleting user: {str(e)}', 500)


# ============================================
# DISABLE/ACTIVATE USER (Admin only)
# ============================================
@users_bp.route('/<user_id>/toggle-status', methods=['PUT'])
@admin_required
def toggle_user_status(user_id):
    """
    Enable or disable user account (admin only)
    """
    try:
        user = User.objects(id=user_id).first()
        
        if not user:
            return error_response('User not found', 404)
        
        user.is_active = not user.is_active
        user.save()
        
        status = 'activated' if user.is_active else 'deactivated'
        return success_response(user.to_dict(), f'User {status} successfully', 200)
    
    except Exception as e:
        return error_response(f'Error updating user status: {str(e)}', 500)
