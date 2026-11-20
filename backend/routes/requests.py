# ReWear Clothing System - Requests Routes (Final MongoDB/MongoEngine Version)
# Handles renting, buying, and exchange requests without SQL interference.

from flask import Blueprint, request, jsonify
from datetime import datetime
from models.models import Request, ClothingItem, User, ImpactMetrics
from utils.common import success_response, error_response, sanitize_input, pagination_params
from utils.auth import token_required
from utils.sustainability import SustainabilityCalculator
from flask_jwt_extended import get_jwt_identity

requests_bp = Blueprint('requests', __name__)

# ============================================
# CREATE REQUEST
# ============================================
@requests_bp.route('', methods=['POST'])
@token_required
def create_request():
    try:
        user_id = get_jwt_identity()
        requester_user = User.objects(id=user_id).first()
        if not requester_user:
            return error_response('User not found', 404)

        data = request.get_json()
        
        if not data or 'item_id' not in data or 'request_type' not in data:
            return error_response('Missing required fields', 400)

        if data['request_type'] not in ['rent', 'buy', 'exchange', 'gift']:
            return error_response('Invalid request type', 400)
        
        # MongoDB Fix: Use .objects() instead of .query.get()
        item = ClothingItem.objects(id=data['item_id']).first()
        if not item:
            return error_response('Item not found', 404)
        
        # Security: Cannot request your own item (comparing IDs as strings)
        if str(item.owner.id) == str(user_id):
            return error_response('Cannot request your own item', 400)
        
        if item.status != 'available':
            return error_response('Item is not available', 400)
        
        # Create request using correct MongoEngine field names
        new_request = Request(
            item=item,
            requester=requester_user,
            owner=item.owner,
            request_type=data['request_type'],
            message=sanitize_input(data.get('message', '')),
            rental_days=data.get('rental_days')
        )
        
        # Handle exchange requests
        if data['request_type'] == 'exchange':
            if 'exchange_item_id' not in data:
                return error_response('Exchange item ID required', 400)
            
            ex_item = ClothingItem.objects(id=data['exchange_item_id']).first()
            if not ex_item or str(ex_item.owner.id) != str(user_id) or ex_item.status != 'available':
                return error_response('Invalid exchange item selected', 400)
            
            new_request.exchange_item = ex_item
        
        # MongoDB Fix: Use .save() instead of db.session.add/commit
        new_request.save()
        
        return success_response(new_request.to_dict(), 'Request created successfully', 201)
    
    except Exception as e:
        return error_response(f'Error creating request: {str(e)}', 500)

# ============================================
# UPDATE REQUEST STATUS (Accept/Reject)
# ============================================
@requests_bp.route('/<request_id>', methods=['PUT'])
@token_required
def update_request(request_id):
    try:
        user_id = get_jwt_identity()
        
        # MongoDB Fix: Use .objects() instead of .query.get()
        req = Request.objects(id=request_id).first()
        
        if not req:
            return error_response('Request not found', 404)
        
        # Permission Check: Only the item owner can accept/reject
        if str(req.owner.id) != str(user_id):
            return error_response('Permission denied', 403)
        
        data = request.get_json()
        status = data.get('status')
        valid_statuses = ['accepted', 'rejected', 'cancelled', 'completed']
        
        if not status or status not in valid_statuses:
            return error_response('Invalid or missing status', 400)
        
        req.status = status
        req.responded_at = datetime.utcnow()
        
        # Logic: If request is accepted, change the item's availability
        if status == 'accepted':
            item = req.item
            if item:
                status_map = {'rent': 'rented', 'buy': 'sold', 'exchange': 'exchanged'}
                item.status = status_map.get(req.request_type, 'available')
                item.save()
                
                # Update Sustainability Impact
                try:
                    # Calculate impact values
                    # If it's a rental, we might want to consider rental days, 
                    # but for simplicity we'll use the per-item constants as defined in the logic
                    co2_saved = item.carbon_impact_kg or 3.0
                    water_saved = item.water_impact_liters or 7000.0
                    
                    # Update Owner (Seller/Lender)
                    owner = req.owner
                    if req.request_type == 'buy':
                        owner.items_sold += 1
                        owner.carbon_saved_kg += co2_saved
                        owner.water_saved_liters += water_saved
                    elif req.request_type == 'rent':
                        owner.items_rented += 1
                        owner.carbon_saved_kg += co2_saved
                        owner.water_saved_liters += water_saved
                    elif req.request_type == 'exchange' and req.exchange_item:
                        owner.items_exchanged += 1
                        # Owner gets impact from the item they RECEIVED
                        ex_item = req.exchange_item
                        owner.carbon_saved_kg += (ex_item.carbon_impact_kg or 3.0)
                        owner.water_saved_liters += (ex_item.water_impact_liters or 7000.0)
                        
                        # Mark exchange item as unavailable too
                        ex_item.status = 'exchanged'
                        ex_item.save()
                    
                    owner.reputation_score += 10 # Base points for successful transaction
                    owner.save()
                    
                    # Update Requester (Buyer/Renter/Exchanger)
                    requester = req.requester
                    if req.request_type == 'buy':
                        requester.items_reworn += 1
                    elif req.request_type == 'rent':
                        requester.items_rented += 1
                    elif req.request_type == 'exchange':
                        requester.items_exchanged += 1
                        # Requester already got items_reworn? No, let's use items_exchanged
                    
                    requester.carbon_saved_kg += co2_saved
                    requester.water_saved_liters += water_saved
                    requester.save()
                    
                    # Create Impact Metrics record
                    action_map = {
                        'rent': 'item_rented',
                        'buy': 'item_sold',
                        'exchange': 'item_exchanged'
                    }
                    
                    impact = ImpactMetrics(
                        user=requester,
                        item=item,
                        action_type=action_map.get(req.request_type, 'item_sold'),
                        co2_reduced_kg=co2_saved,
                        water_saved_liters=water_saved,
                        textile_waste_prevented_kg=0.5 # Constant for now
                    )
                    impact.save()
                    
                except Exception as e:
                    # Log error but don't fail the request acceptance
                    print(f"Error updating impact metrics: {str(e)}")
        
        req.save()
        return success_response(req.to_dict(), f'Request {status} successfully', 200)
    
    except Exception as e:
        return error_response(f'Error updating request: {str(e)}', 500)

# ============================================
# GET USER'S REQUESTS (Sent or Received)
# ============================================
@requests_bp.route('/user/<sort_type>', methods=['GET'])
@token_required
def get_user_requests(sort_type):
    try:
        user_id = get_jwt_identity()
        page, per_page = pagination_params(request)
        
        # Define filters based on whether the user is the one who sent or received
        if sort_type == 'sent':
            filters = {'requester': user_id}
        elif sort_type == 'received':
            filters = {'owner': user_id}
        else:
            return error_response('Invalid sort type', 400)
        
        # Support status filtering (e.g., ?status=pending)
        status_filter = request.args.get('status')
        if status_filter:
            filters['status'] = status_filter

        # MongoDB Pagination logic
        total = Request.objects(**filters).count()
        requests_list = Request.objects(**filters).order_by('-requested_at').skip((page-1)*per_page).limit(per_page)
        
        return success_response({
            'requests': [r.to_dict() for r in requests_list],
            'pagination': {
                'total': total,
                'page': page,
                'per_page': per_page,
                'pages': (total + per_page - 1) // per_page
            }
        }, 'Requests retrieved successfully', 200)
    
    except Exception as e:
        return error_response(f'Error retrieving requests: {str(e)}', 500)

# ============================================
# DASHBOARD STATISTICS
# ============================================
@requests_bp.route('/stats/summary', methods=['GET'])
@token_required
def get_request_statistics():
    try:
        user_id = get_jwt_identity()
        
        stats = {
            'sent': {
                'pending': Request.objects(requester=user_id, status='pending').count(),
                'accepted': Request.objects(requester=user_id, status='accepted').count(),
                'completed': Request.objects(requester=user_id, status='completed').count()
            },
            'received': {
                'pending': Request.objects(owner=user_id, status='pending').count()
            }
        }
        
        return success_response(stats, 'Statistics retrieved successfully', 200)
    except Exception as e:
        return error_response(str(e), 500)

# ============================================
# GET SINGLE REQUEST
# ============================================
@requests_bp.route('/<request_id>', methods=['GET'])
@token_required
def get_request(request_id):
    try:
        req = Request.objects(id=request_id).first()
        if not req:
            return error_response('Request not found', 404)
        return success_response(req.to_dict(), 'Request retrieved', 200)
    except Exception as e:
        return error_response(str(e), 500)
