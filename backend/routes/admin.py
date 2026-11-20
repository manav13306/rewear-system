# ReWear Clothing System - Admin Routes
# Administrative management endpoints

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from mongoengine.errors import OperationError
from models.models import User, ClothingItem, Request, Order, ImpactMetrics
from utils.common import success_response, error_response, pagination_params
from utils.auth import admin_required
from utils.sustainability import ImpactReport

admin_bp = Blueprint('admin', __name__)

# ============================================
# ADMIN DASHBOARD STATISTICS
# ============================================
@admin_bp.route('/dashboard', methods=['GET'])
@admin_required
def admin_dashboard():
    """
    Get admin dashboard with system statistics
    """
    try:
        total_users = User.objects.count()
        active_users = User.objects(is_active=True).count()
        total_items = ClothingItem.objects.count()
        available_items = ClothingItem.objects(status='available').count()
        pending_requests = Request.objects(status='pending').count()
        total_orders = Order.objects.count()
        
        # Calculate global impact
        users = User.objects()
        impact = ImpactReport.get_global_impact_summary(users)
        
        return success_response({
            'users': {
                'total': total_users,
                'active': active_users
            },
            'items': {
                'total': total_items,
                'available': available_items
            },
            'requests': {
                'pending': pending_requests,
                'total': Request.objects.count()
            },
            'orders': {
                'total': total_orders
            },
            'impact': impact
        }, 'Dashboard retrieved', 200)
    
    except Exception as e:
        return error_response(f'Error retrieving dashboard: {str(e)}', 500)


# ============================================
# MODERATE CLOTHING ITEMS
# ============================================
@admin_bp.route('/items/<item_id>/moderate', methods=['PUT'])
@admin_required
def moderate_item(item_id):
    """
    Approve/reject/remove clothing item
    
    Request JSON:
    {
        "action": "approve|reject|remove",
        "reason": "string (optional)"
    }
    """
    try:
        item = ClothingItem.objects(id=item_id).first()
        
        if not item:
            return error_response('Item not found', 404)
        
        data = request.get_json()
        
        if 'action' not in data:
            return error_response('Action required', 400)
        
        action = data['action']
        
        if action == 'remove':
            item.delete()
            return success_response({}, f'Item removed successfully', 200)
        elif action == 'reject':
            item.status = 'inactive'
        elif action == 'approve':
            item.status = 'available'
        else:
            return error_response('Invalid action', 400)
        
        item.save()
        
        return success_response(item.to_dict(), f'Item {action}ed successfully', 200)
    
    except Exception as e:
        return error_response(f'Error moderating item: {str(e)}', 500)


# ============================================
# LIST FLAGGED/REPORTED CONTENT
# ============================================
@admin_bp.route('/reported-items', methods=['GET'])
@admin_required
def get_reported_items():
    """
    Get items that have been flagged or reported
    """
    try:
        page, per_page = pagination_params(request)
        
        # Get inactive or suspicious items
        query = ClothingItem.objects(status='inactive').order_by('-updated_at')
        total = query.count()
        items = query.skip((page-1)*per_page).limit(per_page)
        
        total_pages = (total + per_page - 1) // per_page
        
        return success_response({
            'items': [item.to_dict() for item in items],
            'pagination': {
                'total': total,
                'pages': total_pages,
                'current_page': page,
                'per_page': per_page,
                'has_next': page < total_pages,
                'has_prev': page > 1
            }
        }, 'Reported items retrieved', 200)
    
    except Exception as e:
        return error_response(f'Error retrieving reported items: {str(e)}', 500)


# ============================================
# MANAGE USERS (Disable/Enable)
# ============================================
@admin_bp.route('/users/<user_id>/manage', methods=['PUT'])
@admin_required
def manage_user(user_id):
    """
    Enable/disable/delete user account
    
    Request JSON:
    {
        "action": "enable|disable|delete",
        "reason": "string (optional)"
    }
    """
    try:
        user = User.objects(id=user_id).first()
        
        if not user:
            return error_response('User not found', 404)
        
        data = request.get_json()
        
        if 'action' not in data:
            return error_response('Action required', 400)
        
        action = data['action']
        
        if action == 'enable':
            user.is_active = True
            user.save()
        elif action == 'disable':
            user.is_active = False
            user.save()
        elif action == 'delete':
            try:
                user.delete()
                return success_response({}, f'User deleted successfully', 200)
            except OperationError:
                user.is_active = False
                user.save()
                return success_response(user.to_dict(), 'User has related records and was deactivated', 200)
        else:
            return error_response('Invalid action', 400)
        
        return success_response(user.to_dict(), f'User {action}d successfully', 200)
    
    except Exception as e:
        return error_response(f'Error managing user: {str(e)}', 500)


# ============================================
# VIEW SYSTEM REQUESTS
# ============================================
@admin_bp.route('/requests', methods=['GET'])
@admin_required
def get_all_requests():
    """
    Get all system requests (admin view)
    """
    try:
        page, per_page = pagination_params(request)
        
        # Filter options
        status = request.args.get('status')
        request_type = request.args.get('request_type')
        
        filters = {}
        if status:
            filters['status'] = status
        if request_type:
            filters['request_type'] = request_type
        
        query = Request.objects(**filters).order_by('-requested_at')
        total = query.count()
        requests_list = query.skip((page-1)*per_page).limit(per_page)
        
        total_pages = (total + per_page - 1) // per_page
        
        return success_response({
            'requests': [req.to_dict() for req in requests_list],
            'pagination': {
                'total': total,
                'pages': total_pages,
                'current_page': page,
                'per_page': per_page,
                'has_next': page < total_pages,
                'has_prev': page > 1
            }
        }, 'Requests retrieved', 200)
    
    except Exception as e:
        return error_response(f'Error retrieving requests: {str(e)}', 500)


# ============================================
# VIEW SYSTEM ORDERS
# ============================================
@admin_bp.route('/orders', methods=['GET'])
@admin_required
def get_all_orders():
    """
    Get all system orders (admin view)
    """
    try:
        page, per_page = pagination_params(request)
        
        # Filter options
        status = request.args.get('status')
        order_type = request.args.get('order_type')
        
        filters = {}
        if status:
            filters['status'] = status
        if order_type:
            filters['order_type'] = order_type
        
        query = Order.objects(**filters).order_by('-order_date')
        total = query.count()
        orders = query.skip((page-1)*per_page).limit(per_page)
        
        total_pages = (total + per_page - 1) // per_page
        
        return success_response({
            'orders': [order.to_dict() for order in orders],
            'pagination': {
                'total': total,
                'pages': total_pages,
                'current_page': page,
                'per_page': per_page,
                'has_next': page < total_pages,
                'has_prev': page > 1
            }
        }, 'Orders retrieved', 200)
    
    except Exception as e:
        return error_response(f'Error retrieving orders: {str(e)}', 500)


# ============================================
# SYSTEM CLEANUP
# ============================================
@admin_bp.route('/cleanup', methods=['POST'])
@admin_required
def system_cleanup():
    """
    Perform system cleanup (delete old records, etc.)
    """
    try:
        # Delete requests older than 6 months
        six_months_ago = datetime.utcnow() - timedelta(days=180)
        deleted_count = Request.objects(
            status__in=['rejected', 'cancelled'],
            requested_at__lt=six_months_ago
        ).delete()
        
        return success_response({
            'deleted_requests': deleted_count
        }, 'Cleanup completed', 200)
    
    except Exception as e:
        return error_response(f'Error during cleanup: {str(e)}', 500)
