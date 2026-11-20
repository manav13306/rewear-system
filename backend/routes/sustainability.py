# ReWear Clothing System - Sustainability/Impact Routes (MongoDB Version)
from flask import Blueprint, jsonify
from models.models import ClothingItem, Request, User
from utils.common import success_response, error_response
from utils.auth import token_required

sustainability_bp = Blueprint('sustainability', __name__)

@sustainability_bp.route('/user/<user_id>', methods=['GET'])
@token_required
def get_user_impact(user_id):
    """
    Calculate the environmental impact for a specific user based on their items
    """
    try:
        # Find all items owned by this user
        user_items = ClothingItem.objects(owner=user_id)
        
        # Calculate totals
        total_items = user_items.count()
        total_co2_saved = sum(item.carbon_impact_kg for item in user_items if item.carbon_impact_kg)
        total_water_saved = sum(item.water_impact_liters for item in user_items if item.water_impact_liters)
        
        # Count transactions (rented or sold)
        rented_count = user_items.filter(status='rented').count()
        sold_count = user_items.filter(status='sold').count()
        
        return success_response({
            'total_items_reworn': total_items,
            'total_items_rented': rented_count,
            'total_items_sold': sold_count,
            'carbon_saved_kg': total_co2_saved,
            'water_saved_liters': total_water_saved
        }, 'Impact data retrieved successfully', 200)
        
    except Exception as e:
        return error_response(f'Error calculating impact: {str(e)}', 500)