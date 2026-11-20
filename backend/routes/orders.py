# ReWear Clothing System - Orders Routes
# Order management and transaction tracking endpoints

from flask import Blueprint, request, jsonify
from datetime import datetime
from mongoengine import Q
from models.models import Order, Request, ClothingItem, User
from utils.common import success_response, error_response, sanitize_input, pagination_params
from utils.auth import token_required
from flask_jwt_extended import get_jwt_identity

orders_bp = Blueprint('orders', __name__)

# ============================================
# CREATE ORDER
# ============================================
@orders_bp.route('', methods=['POST'])
@token_required
def create_order():
    """
    Create an order from an accepted request
    
    Request JSON:
    {
        "request_id": "string",
        "delivery_address": "string"
    }
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        if not data or 'request_id' not in data or 'delivery_address' not in data:
            return error_response('Missing required fields', 400)
        
        # Get request
        req = Request.objects(id=data['request_id']).first()
        if not req:
            return error_response('Request not found', 404)
        
        # Check if request is accepted
        if req.status != 'accepted':
            return error_response('Request must be accepted before creating order', 400)
        
        # Check if order already exists
        existing_order = Order.objects(request=req).first()
        if existing_order:
            return error_response('Order already exists for this request', 409)
        
        item = req.item
        
        # Determine order type mapping
        type_map = {'rent': 'rental', 'buy': 'purchase', 'exchange': 'exchange'}
        order_type = type_map.get(req.request_type, 'purchase')
        
        # Create order
        order = Order(
            request=req,
            item=item,
            buyer=req.requester,
            seller=req.owner,
            order_type=order_type,
            total_amount=item.price if req.request_type == 'buy' else 0,
            delivery_address=sanitize_input(data['delivery_address'])
        )
        
        order.save()
        
        return success_response(order.to_dict(), 'Order created successfully', 201)
    
    except Exception as e:
        return error_response(f'Error creating order: {str(e)}', 500)


# ============================================
# GET USER'S ORDERS
# ============================================
@orders_bp.route('/user/<user_id>', methods=['GET'])
@token_required
def get_user_orders(user_id):
    """
    Get order history for a user (as buyer or seller)
    """
    try:
        current_user_id = get_jwt_identity()
        current_user = User.objects(id=current_user_id).first()
        if not current_user:
            return error_response('User not found', 404)

        # Only owner of the orders or admin can access this endpoint
        if str(current_user_id) != str(user_id) and current_user.role != 'admin':
            return error_response('Permission denied', 403)

        page, per_page = pagination_params(request)
        
        # Get orders where user is buyer or seller
        query = Order.objects(Q(buyer=user_id) | Q(seller=user_id)).order_by('-order_date')
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
        }, 'Orders retrieved successfully', 200)
    
    except Exception as e:
        return error_response(f'Error retrieving orders: {str(e)}', 500)


# ============================================
# GET ORDER DETAILS
# ============================================
@orders_bp.route('/<order_id>', methods=['GET'])
@token_required
def get_order_details(order_id):
    """
    Get detailed order information
    """
    try:
        user_id = get_jwt_identity()
        order = Order.objects(id=order_id).first()
        
        if not order:
            return error_response('Order not found', 404)
        
        # Permission check - buyer, seller, or admin
        if str(order.buyer.id) != str(user_id) and str(order.seller.id) != str(user_id):
            return error_response('Permission denied', 403)
        
        return success_response(order.to_dict(), 'Order retrieved successfully', 200)
    
    except Exception as e:
        return error_response(f'Error retrieving order: {str(e)}', 500)


# ============================================
# UPDATE ORDER STATUS
# ============================================
@orders_bp.route('/<order_id>/status', methods=['PUT'])
@token_required
def update_order_status(order_id):
    """
    Update order status (seller or buyer)
    
    Request JSON:
    {
        "status": "confirmed|shipped|delivered|returned|cancelled",
        "tracking_number": "string (optional)"
    }
    """
    try:
        user_id = get_jwt_identity()
        order = Order.objects(id=order_id).first()
        
        if not order:
            return error_response('Order not found', 404)
        
        # Permission check
        if str(order.seller.id) != str(user_id) and str(order.buyer.id) != str(user_id):
            return error_response('Permission denied', 403)
        
        data = request.get_json()
        
        if 'status' not in data:
            return error_response('Status required', 400)
        
        valid_statuses = ['confirmed', 'shipped', 'delivered', 'returned', 'cancelled']
        if data['status'] not in valid_statuses:
            return error_response('Invalid status', 400)
        
        order.status = data['status']
        
        # Update timestamps based on status
        if data['status'] == 'shipped':
            order.shipped_date = datetime.utcnow()
        elif data['status'] == 'delivered':
            order.delivered_date = datetime.utcnow()
        elif data['status'] == 'returned':
            order.return_date = datetime.utcnow()
        
        # Update tracking number if provided
        if 'tracking_number' in data:
            order.tracking_number = data['tracking_number']
        
        order.save()
        
        return success_response(order.to_dict(), 'Order status updated successfully', 200)
    
    except Exception as e:
        return error_response(f'Error updating order: {str(e)}', 500)


# ============================================
# GET ORDER STATISTICS
# ============================================
@orders_bp.route('/stats/summary', methods=['GET'])
@token_required
def get_order_statistics():
    """
    Get order statistics for current user
    """
    try:
        user_id = get_jwt_identity()
        
        # Orders as buyer
        purchased = Order.objects(buyer=user_id).count()
        
        # Orders as seller
        sold = Order.objects(seller=user_id).count()
        
        # Completed orders
        completed = Order.objects(
            (Q(buyer=user_id) | Q(seller=user_id)) & Q(status='delivered')
        ).count()
        
        # Pending orders
        pending = Order.objects(
            (Q(buyer=user_id) | Q(seller=user_id)) & Q(status__in=['pending', 'confirmed', 'shipped'])
        ).count()
        
        return success_response({
            'purchased': purchased,
            'sold': sold,
            'completed': completed,
            'pending': pending
        }, 'Statistics retrieved successfully', 200)
    
    except Exception as e:
        return error_response(f'Error retrieving statistics: {str(e)}', 500)
