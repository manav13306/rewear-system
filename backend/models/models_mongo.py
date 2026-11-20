# ReWear Clothing System - MongoDB Models
# MongoEngine ORM models for all entities

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from mongoengine import (
    Document, StringField, IntField, FloatField, BooleanField,
    DateTimeField, TextAreaField, ReferenceField, ListField,
    EmbeddedDocument, EmbeddedDocumentField, ValidationError,
    DENY, PULL
)

# ============================================
# USER MODEL
# ============================================
class User(Document):
    """
    User model representing system users
    """
    username = StringField(unique=True, required=True)
    email = StringField(unique=True, required=True)
    password_hash = StringField(required=True)
    full_name = StringField(required=True)
    mobile = StringField()
    address = StringField()
    profile_image_url = StringField()
    bio = StringField()
    role = StringField(choices=['user', 'admin'], default='user')
    
    # Sustainability metrics
    carbon_saved_kg = FloatField(default=0)
    water_saved_liters = FloatField(default=0)
    items_reworn = IntField(default=0)
    items_rented = IntField(default=0)
    items_sold = IntField(default=0)
    reputation_score = IntField(default=0)
    
    is_active = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'users',
        'indexes': [
            'username',
            'email',
            'role',
            'created_at'
        ]
    }
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': str(self.id),
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'mobile': self.mobile,
            'address': self.address,
            'profile_image_url': self.profile_image_url,
            'bio': self.bio,
            'role': self.role,
            'carbon_saved_kg': self.carbon_saved_kg,
            'water_saved_liters': self.water_saved_liters,
            'items_reworn': self.items_reworn,
            'items_rented': self.items_rented,
            'items_sold': self.items_sold,
            'reputation_score': self.reputation_score,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<User {self.username}>'


# ============================================
# CLOTHING ITEM MODEL
# ============================================
class ClothingItem(Document):
    """
    Clothing items available for rent/sell/exchange
    """
    owner = ReferenceField(User, required=True, reverse_delete_rule=DENY)
    
    # Item details
    title = StringField(required=True)
    description = StringField()
    category = StringField(required=True)  # tops, bottoms, dresses, etc.
    size = StringField(required=True)
    color = StringField()
    brand = StringField()
    
    # Condition and status
    condition = StringField(required=True, choices=['new', 'like_new', 'good', 'fair', 'worn'])
    rewear_count = IntField(default=0)
    
    # Transaction details
    transaction_type = StringField(required=True, choices=['rent', 'sell', 'exchange', 'free'])
    price = FloatField()
    rental_price_per_day = FloatField()
    
    # Media
    image_url = StringField()
    
    # Availability
    status = StringField(default='available', choices=['available', 'rented', 'sold', 'exchanged', 'inactive'])
    
    # Sustainability impact
    carbon_impact_kg = FloatField(default=0)
    water_impact_liters = FloatField(default=0)
    
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'clothing_items',
        'indexes': [
            'owner',
            'category',
            'status',
            'transaction_type',
            'created_at'
        ]
    }
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': str(self.id),
            'owner_id': str(self.owner.id) if self.owner else None,
            'owner': self.owner.to_dict() if self.owner else None,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'size': self.size,
            'color': self.color,
            'brand': self.brand,
            'condition': self.condition,
            'rewear_count': self.rewear_count,
            'transaction_type': self.transaction_type,
            'price': self.price,
            'rental_price_per_day': self.rental_price_per_day,
            'image_url': self.image_url,
            'status': self.status,
            'carbon_impact_kg': self.carbon_impact_kg,
            'water_impact_liters': self.water_impact_liters,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<ClothingItem {self.title}>'


# ============================================
# REQUEST MODEL
# ============================================
class Request(Document):
    """
    Requests for renting, buying, or exchanging items
    """
    item = ReferenceField(ClothingItem, required=True, reverse_delete_rule=DENY)
    requester = ReferenceField(User, required=True, reverse_delete_rule=DENY)
    owner = ReferenceField(User, required=True, reverse_delete_rule=DENY)
    
    # Request details
    request_type = StringField(required=True, choices=['rent', 'buy', 'exchange', 'gift'])
    status = StringField(default='pending', choices=['pending', 'accepted', 'rejected', 'cancelled', 'completed'])
    
    message = StringField()
    rental_days = IntField()
    exchange_item = ReferenceField(ClothingItem)
    
    # Timestamps
    requested_at = DateTimeField(default=datetime.utcnow)
    responded_at = DateTimeField()
    completed_at = DateTimeField()
    
    meta = {
        'collection': 'requests',
        'indexes': [
            'item',
            'requester',
            'owner',
            'status',
            'request_type',
            'requested_at'
        ]
    }
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': str(self.id),
            'item_id': str(self.item.id) if self.item else None,
            'item': self.item.to_dict() if self.item else None,
            'requester_id': str(self.requester.id) if self.requester else None,
            'requester': self.requester.to_dict() if self.requester else None,
            'owner_id': str(self.owner.id) if self.owner else None,
            'owner': self.owner.to_dict() if self.owner else None,
            'request_type': self.request_type,
            'status': self.status,
            'message': self.message,
            'rental_days': self.rental_days,
            'exchange_item_id': str(self.exchange_item.id) if self.exchange_item else None,
            'requested_at': self.requested_at.isoformat(),
            'responded_at': self.responded_at.isoformat() if self.responded_at else None
        }
    
    def __repr__(self):
        return f'<Request {self.id} - {self.request_type}>'


# ============================================
# ORDER MODEL
# ============================================
class Order(Document):
    """
    Orders for completed transactions
    """
    request = ReferenceField(Request, required=True)
    item = ReferenceField(ClothingItem, required=True, reverse_delete_rule=DENY)
    buyer = ReferenceField(User, required=True, reverse_delete_rule=DENY)
    seller = ReferenceField(User, required=True, reverse_delete_rule=DENY)
    
    # Transaction details
    order_type = StringField(required=True, choices=['purchase', 'rental', 'exchange'])
    total_amount = FloatField()
    commission = FloatField(default=0)
    
    # Status
    status = StringField(default='pending', choices=['pending', 'confirmed', 'shipped', 'delivered', 'returned', 'cancelled'])
    
    # Shipping details
    delivery_address = StringField(required=True)
    tracking_number = StringField()
    
    # Timestamps
    order_date = DateTimeField(default=datetime.utcnow)
    shipped_date = DateTimeField()
    delivered_date = DateTimeField()
    return_date = DateTimeField()
    
    meta = {
        'collection': 'orders',
        'indexes': [
            'buyer',
            'seller',
            'status',
            'order_date'
        ]
    }
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': str(self.id),
            'request_id': str(self.request.id) if self.request else None,
            'item_id': str(self.item.id) if self.item else None,
            'item': self.item.to_dict() if self.item else None,
            'buyer_id': str(self.buyer.id) if self.buyer else None,
            'seller_id': str(self.seller.id) if self.seller else None,
            'order_type': self.order_type,
            'total_amount': self.total_amount,
            'commission': self.commission,
            'status': self.status,
            'delivery_address': self.delivery_address,
            'tracking_number': self.tracking_number,
            'order_date': self.order_date.isoformat(),
            'shipped_date': self.shipped_date.isoformat() if self.shipped_date else None,
            'delivered_date': self.delivered_date.isoformat() if self.delivered_date else None
        }
    
    def __repr__(self):
        return f'<Order {self.id}>'


# ============================================
# IMPACT METRICS MODEL
# ============================================
class ImpactMetrics(Document):
    """
    Track sustainability impact of user actions
    """
    user = ReferenceField(User, required=True, reverse_delete_rule=DENY)
    item = ReferenceField(ClothingItem, reverse_delete_rule=PULL)
    
    # Action type
    action_type = StringField(required=True, choices=['item_reworn', 'item_rented', 'item_sold', 'item_exchanged'])
    
    # Impact data
    co2_reduced_kg = FloatField(required=True)
    water_saved_liters = FloatField(required=True)
    textile_waste_prevented_kg = FloatField(default=0)
    
    created_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'impact_metrics',
        'indexes': [
            'user',
            'action_type',
            'created_at'
        ]
    }
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': str(self.id),
            'user_id': str(self.user.id) if self.user else None,
            'item_id': str(self.item.id) if self.item else None,
            'action_type': self.action_type,
            'co2_reduced_kg': self.co2_reduced_kg,
            'water_saved_liters': self.water_saved_liters,
            'textile_waste_prevented_kg': self.textile_waste_prevented_kg,
            'created_at': self.created_at.isoformat()
        }


# ============================================
# REVIEW MODEL
# ============================================
class Review(Document):
    """
    User reviews and ratings
    """
    reviewer = ReferenceField(User, required=True, reverse_delete_rule=DENY)
    reviewed_user = ReferenceField(User, required=True, reverse_delete_rule=DENY)
    order = ReferenceField(Order)
    
    rating = IntField(required=True, min_value=1, max_value=5)
    review_text = StringField()
    
    created_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'reviews',
        'indexes': [
            'reviewer',
            'reviewed_user',
            'created_at'
        ]
    }
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': str(self.id),
            'reviewer_id': str(self.reviewer.id) if self.reviewer else None,
            'reviewer': self.reviewer.to_dict() if self.reviewer else None,
            'reviewed_user_id': str(self.reviewed_user.id) if self.reviewed_user else None,
            'rating': self.rating,
            'review_text': self.review_text,
            'created_at': self.created_at.isoformat()
        }


# ============================================
# WISHLIST MODEL
# ============================================
class Wishlist(Document):
    """
    User wishlists
    """
    user = ReferenceField(User, required=True, reverse_delete_rule=DENY)
    item = ReferenceField(ClothingItem, required=True, reverse_delete_rule=DENY)
    added_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'wishlist',
        'indexes': [
            ('user', 'item'),  # Unique compound index
            'user'
        ]
    }
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': str(self.id),
            'user_id': str(self.user.id) if self.user else None,
            'item_id': str(self.item.id) if self.item else None,
            'item': self.item.to_dict() if self.item else None,
            'added_at': self.added_at.isoformat()
        }


# ============================================
# NOTIFICATION MODEL
# ============================================
class Notification(Document):
    """
    User notifications
    """
    user = ReferenceField(User, required=True, reverse_delete_rule=DENY)
    title = StringField(required=True)
    message = StringField(required=True)
    notification_type = StringField(default='system', choices=['order', 'request', 'message', 'system'])
    is_read = BooleanField(default=False)
    
    created_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'notifications',
        'indexes': [
            'user',
            'is_read',
            'created_at'
        ]
    }
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': str(self.id),
            'user_id': str(self.user.id) if self.user else None,
            'title': self.title,
            'message': self.message,
            'notification_type': self.notification_type,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat()
        }
