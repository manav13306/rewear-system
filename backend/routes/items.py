# ReWear Clothing System - Clothing Items Routes
from datetime import datetime

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity
from mongoengine import Q
from mongoengine.errors import OperationError

from models.models import ClothingItem, User
from utils.auth import token_required
from utils.common import error_response, pagination_params, sanitize_input, success_response
from utils.sustainability import SustainabilityCalculator

items_bp = Blueprint("items", __name__)


def _normalize_filter(value):
    if value is None:
        return None
    normalized = str(value).strip().lower()
    if normalized in {"", "all", "all categories", "all conditions", "all types"}:
        return None
    return normalized


@items_bp.route("", methods=["GET"])
def get_items():
    """
    Retrieve paginated items with optional filtering and search.
    """
    try:
        page, per_page = pagination_params(request)
        search = request.args.get("search", "", type=str).strip()

        category = _normalize_filter(request.args.get("category"))
        condition = _normalize_filter(request.args.get("condition"))
        transaction_type = _normalize_filter(request.args.get("transaction_type"))

        query = Q(status="available")

        if category:
            query &= Q(category=category)
        if condition:
            query &= Q(condition=condition)
        if transaction_type:
            query &= Q(transaction_type=transaction_type)
        if search:
            query &= (
                Q(title__icontains=search)
                | Q(description__icontains=search)
                | Q(brand__icontains=search)
            )

        queryset = ClothingItem.objects(query).order_by("-created_at")
        total = queryset.count()
        items = queryset.skip((page - 1) * per_page).limit(per_page)
        total_pages = (total + per_page - 1) // per_page

        return success_response(
            {
                "items": [item.to_dict() for item in items],
                "pagination": {
                    "total": total,
                    "pages": total_pages,
                    "current_page": page,
                    "per_page": per_page,
                    "has_next": page < total_pages,
                    "has_prev": page > 1,
                },
            },
            "Items retrieved successfully",
            200,
        )
    except Exception:
        return error_response("Error retrieving items", 500)


@items_bp.route("/user/<user_id>", methods=["GET"])
def get_user_items(user_id):
    """Retrieve items uploaded by a specific user."""
    try:
        page, per_page = pagination_params(request)

        user = User.objects(id=user_id).first()
        if not user:
            return error_response("User not found", 404)

        queryset = ClothingItem.objects(owner=user).order_by("-created_at")
        total = queryset.count()
        items = queryset.skip((page - 1) * per_page).limit(per_page)
        total_pages = (total + per_page - 1) // per_page

        return success_response(
            {
                "items": [item.to_dict() for item in items],
                "pagination": {
                    "total": total,
                    "pages": total_pages,
                    "current_page": page,
                    "per_page": per_page,
                    "has_next": page < total_pages,
                    "has_prev": page > 1,
                },
            },
            "User items retrieved successfully",
            200,
        )
    except Exception:
        return error_response("Error retrieving user items", 500)


@items_bp.route("", methods=["POST"])
@token_required
def create_item():
    try:
        user_id = get_jwt_identity()
        user = User.objects(id=user_id).first()
        if not user:
            return error_response("User not found", 404)

        data = request.get_json() or {}

        required_fields = [
            "title",
            "description",
            "category",
            "size",
            "condition",
            "transaction_type",
        ]
        if not all(data.get(field) for field in required_fields):
            return error_response("Missing required fields", 400)

        transaction_type = str(data["transaction_type"]).strip().lower()
        valid_types = {"rent", "buy", "exchange", "free"}
        if transaction_type not in valid_types:
            return error_response("Invalid transaction type", 400)

        condition = str(data["condition"]).strip().lower()
        valid_conditions = {"new", "like_new", "good", "fair", "worn"}
        if condition not in valid_conditions:
            return error_response("Invalid condition", 400)

        try:
            price = float(data.get("price", 0) or 0)
            rental_price_per_day = float(data.get("rental_price_per_day", 0) or 0)
        except (TypeError, ValueError):
            return error_response("Price fields must be numeric", 400)

        if price < 0 or rental_price_per_day < 0:
            return error_response("Price values cannot be negative", 400)

        item = ClothingItem(
            owner=user,
            title=sanitize_input(data["title"]),
            description=sanitize_input(data["description"]),
            category=sanitize_input(data["category"]).lower(),
            size=sanitize_input(data["size"]),
            color=sanitize_input(data.get("color", "")),
            brand=sanitize_input(data.get("brand", "")),
            condition=condition,
            transaction_type=transaction_type,
            price=price,
            rental_price_per_day=rental_price_per_day,
            image_url=sanitize_input(data.get("image_url", "")),
            exchange_preferences=sanitize_input(data.get("exchange_preferences", "")),
            status="available",
            updated_at=datetime.utcnow(),
        )

        calculator = SustainabilityCalculator()
        item.carbon_impact_kg = calculator.CO2_PER_ITEM_KG
        item.water_impact_liters = calculator.WATER_PER_ITEM_LITERS

        item.save()
        return success_response(item.to_dict(), "Item uploaded successfully", 201)

    except Exception:
        return error_response("Error creating item", 500)


@items_bp.route("/<item_id>", methods=["GET"])
def get_item_details(item_id):
    try:
        item = ClothingItem.objects(id=item_id).first()
        if not item:
            return error_response("Item not found", 404)

        return success_response(item.to_dict(), "Item retrieved successfully", 200)
    except Exception:
        return error_response("Error fetching item details", 500)


@items_bp.route("/<item_id>", methods=["DELETE"])
@token_required
def delete_item(item_id):
    try:
        user_id = get_jwt_identity()
        item = ClothingItem.objects(id=item_id).first()

        if not item:
            return error_response("Item not found", 404)

        if str(item.owner.id) != str(user_id):
            return error_response("Unauthorized", 403)

        try:
            item.delete()
            return success_response({}, "Item deleted successfully", 200)
        except OperationError:
            # Keep historical references intact for completed transactions.
            item.status = "inactive"
            item.updated_at = datetime.utcnow()
            item.save()
            return success_response(
                item.to_dict(),
                "Item has related transactions and was archived instead of deleted",
                200,
            )
    except Exception:
        return error_response("Error deleting item", 500)
