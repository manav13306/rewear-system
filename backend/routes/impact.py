# ReWear Clothing System - Sustainability Impact Routes
# Environmental metrics and reporting endpoints

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from models.models import User, ImpactMetrics, ClothingItem
from utils.common import success_response, error_response, pagination_params
from utils.auth import token_required
from utils.sustainability import ImpactReport, SustainabilityCalculator
from flask_jwt_extended import get_jwt_identity

impact_bp = Blueprint('impact', __name__)

# ============================================
# GET GLOBAL IMPACT SUMMARY
# ============================================
@impact_bp.route('/summary', methods=['GET'])
def get_global_impact():
    """
    Get global environmental impact summary
    """
    try:
        # Get all active users
        users = User.objects(is_active=True)
        
        # Count all clothing items (available or not)
        total_items_listed = ClothingItem.objects().count()
        
        impact_summary = ImpactReport.get_global_impact_summary(users, total_items_listed)
        
        return success_response(impact_summary, 'Global impact summary retrieved', 200)
    
    except Exception as e:
        return error_response(f'Error retrieving global impact: {str(e)}', 500)


# ============================================
# GET USER'S SUSTAINABILITY IMPACT
# ============================================
@impact_bp.route('/user/<user_id>', methods=['GET'])
def get_user_impact(user_id):
    """
    Get sustainability impact for a specific user
    """
    try:
        user = User.objects(id=user_id).first()
        
        if not user:
            return error_response('User not found', 404)
        
        impact_summary = ImpactReport.get_user_impact_summary(user)
        
        return success_response(impact_summary, 'User impact summary retrieved', 200)
    
    except Exception as e:
        return error_response(f'Error retrieving user impact: {str(e)}', 500)


# ============================================
# GET CURRENT USER'S IMPACT
# ============================================
@impact_bp.route('/me', methods=['GET'])
@token_required
def get_current_user_impact():
    """
    Get current user's sustainability impact
    """
    try:
        user_id = get_jwt_identity()
        user = User.objects(id=user_id).first()
        
        if not user:
            return error_response('User not found', 404)
        
        impact_summary = ImpactReport.get_user_impact_summary(user)
        
        return success_response(impact_summary, 'Current user impact retrieved', 200)
    
    except Exception as e:
        return error_response(f'Error retrieving impact: {str(e)}', 500)


# ============================================
# GET MONTHLY IMPACT STATISTICS
# ============================================
@impact_bp.route('/monthly', methods=['GET'])
def get_monthly_impact():
    """
    Get monthly environmental impact statistics
    """
    try:
        # Get last 12 months
        twelve_months_ago = datetime.utcnow() - timedelta(days=365)
        
        # MongoDB aggregation pipeline
        pipeline = [
            {'$match': {'created_at': {'$gte': twelve_months_ago}}},
            {'$group': {
                '_id': {'$dateToString': {'format': '%Y-%m', 'date': '$created_at'}},
                'total_co2': {'$sum': '$co2_reduced_kg'},
                'total_water': {'$sum': '$water_saved_liters'},
                'actions': {'$sum': 1}
            }},
            {'$sort': {'_id': 1}}
        ]
        
        monthly_stats = ImpactMetrics.objects.aggregate(pipeline)
        
        stats = [
            {
                'month': stat['_id'],
                'co2_reduced_kg': float(stat['total_co2'] or 0),
                'water_saved_liters': float(stat['total_water'] or 0),
                'actions': stat['actions']
            }
            for stat in monthly_stats
        ]
        
        return success_response(stats, 'Monthly statistics retrieved', 200)
    
    except Exception as e:
        return error_response(f'Error retrieving monthly statistics: {str(e)}', 500)


# ============================================
# GET LEADERBOARD (Top eco-friendly users)
# ============================================
@impact_bp.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    """
    Get leaderboard of most eco-friendly users
    """
    try:
        page, per_page = pagination_params(request)
        
        # Sort by carbon saved
        query = User.objects(is_active=True).order_by('-carbon_saved_kg')
        total = query.count()
        users = query.skip((page-1)*per_page).limit(per_page)
        
        total_pages = (total + per_page - 1) // per_page
        
        leaderboard = []
        for idx, user in enumerate(users, start=1 + (page-1)*per_page):
            summary = ImpactReport.get_user_impact_summary(user)
            summary['rank'] = idx
            leaderboard.append(summary)
        
        return success_response({
            'leaderboard': leaderboard,
            'pagination': {
                'total': total,
                'pages': total_pages,
                'current_page': page,
                'per_page': per_page,
                'has_next': page < total_pages,
                'has_prev': page > 1
            }
        }, 'Leaderboard retrieved', 200)
    
    except Exception as e:
        return error_response(f'Error retrieving leaderboard: {str(e)}', 500)


# ============================================
# GET IMPACT METRICS DETAILS
# ============================================
@impact_bp.route('/metrics/<user_id>', methods=['GET'])
def get_impact_metrics(user_id):
    """
    Get detailed impact metrics for a user
    """
    try:
        page, per_page = pagination_params(request)
        
        query = ImpactMetrics.objects(user=user_id).order_by('-created_at')
        total = query.count()
        metrics = query.skip((page-1)*per_page).limit(per_page)
        
        total_pages = (total + per_page - 1) // per_page
        
        return success_response({
            'metrics': [metric.to_dict() for metric in metrics],
            'pagination': {
                'total': total,
                'pages': total_pages,
                'current_page': page,
                'per_page': per_page,
                'has_next': page < total_pages,
                'has_prev': page > 1
            }
        }, 'Metrics retrieved', 200)
    
    except Exception as e:
        return error_response(f'Error retrieving metrics: {str(e)}', 500)


# ============================================
# GET ECO-EQUIVALENTS FOR CO2
# ============================================
@impact_bp.route('/eco-equivalents/co2/<float:co2_kg>', methods=['GET'])
def get_co2_equivalents(co2_kg):
    """
    Get eco-friendly equivalents for CO2 saved
    """
    try:
        calculator = SustainabilityCalculator()
        equivalents = calculator.get_eco_equivalent(co2_kg)
        
        return success_response(equivalents, 'CO2 equivalents calculated', 200)
    
    except Exception as e:
        return error_response(f'Error calculating equivalents: {str(e)}', 500)


# ============================================
# GET WATER EQUIVALENTS
# ============================================
@impact_bp.route('/eco-equivalents/water/<float:water_liters>', methods=['GET'])
def get_water_equivalents(water_liters):
    """
    Get eco-friendly equivalents for water saved
    """
    try:
        calculator = SustainabilityCalculator()
        equivalents = calculator.get_water_equivalent(water_liters)
        
        return success_response(equivalents, 'Water equivalents calculated', 200)
    
    except Exception as e:
        return error_response(f'Error calculating equivalents: {str(e)}', 500)
