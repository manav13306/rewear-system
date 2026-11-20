# ReWear Clothing System - Database Models
# SQLAlchemy ORM models for all entities

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from database import db

# ============================================
# USER MODEL
# ============================================
class User(db.Model):
    """
    User model representing system users
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(15))
    address = db.Column(db.Text)
    profile_image_url = db.Column(db.String(255))
    bio = db.Column(db.Text)
    role = db.Column(db.String(20), default='user', index=True)  # user, admin
    
    # Sustainability metrics
    carbon_saved_kg = db.Column(db.Float, default=0)
    water_saved_liters = db.Column(db.Float, default=0)
    items_reworn = db.Column(db.Integer, default=0)
    items_rented = db.Column(db.Integer, default=0)
    items_sold = db.Column(db.Integer, default=0)
    reputation_score = db.Column(db.Integer, default=0)
    
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    items = db.relationship('ClothingItem', backref='owner', lazy=True, foreign_keys='ClothingItem.user_id')
    requests_made = db.relationship('Request', backref='requester', lazy=True, foreign_keys='Request.requester_id')
    requests_received = db.relationship('Request', backref='owner', lazy=True, foreign_keys='Request.owner_id')
    orders_bought = db.relationship('Order', backref='buyer', lazy=True, foreign_keys='Order.buyer_id')
    orders_sold = db.relationship('Order', backref='seller', lazy=True, foreign_keys='Order.seller_id')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
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
class ClothingItem(db.Model):
    """
    Clothing items available for rent/sell/exchange
    """
    __tablename__ = 'clothing_items'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Item details
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(20), nullable=False, index=True)  # tops, bottoms, dresses, etc.
    size = db.Column(db.String(10), nullable=False)
    color = db.Column(db.String(50))
    brand = db.Column(db.String(50))
    
    # Condition and status
    condition = db.Column(db.String(20), nullable=False)  # new, like_new, good, fair, worn
    rewear_count = db.Column(db.Integer, default=0)
    
    # Transaction details
    transaction_type = db.Column(db.String(20), nullable=False, index=True)  # rent, sell, exchange, free
    price = db.Column(db.Float)
    rental_price_per_day = db.Column(db.Float)
    
    # Media
    image_url = db.Column(db.String(255))
    
    # Availability
    status = db.Column(db.String(20), default='available', index=True)  # available, rented, sold, exchanged, inactive
    
    # Sustainability impact
    carbon_impact_kg = db.Column(db.Float, default=0)
    water_impact_liters = db.Column(db.Float, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    requests = db.relationship('Request', backref='item', lazy=True, foreign_keys='Request.item_id')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
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
class Request(db.Model):
    """
    Requests for renting, buying, or exchanging items
    """
    __tablename__ = 'requests'
    
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('clothing_items.id'), nullable=False, index=True)
    requester_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Request details
    request_type = db.Column(db.String(20), nullable=False, index=True)  # rent, buy, exchange, gift
    status = db.Column(db.String(20), default='pending', index=True)  # pending, accepted, rejected, cancelled, completed
    
    message = db.Column(db.Text)
    rental_days = db.Column(db.Integer)
    exchange_item_id = db.Column(db.Integer, db.ForeignKey('clothing_items.id'))
    
    # Timestamps
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)
    responded_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    
    # Relationships
    order = db.relationship('Order', backref='request', uselist=False, lazy=True)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'item_id': self.item_id,
            'item': self.item.to_dict() if self.item else None,
            'requester_id': self.requester_id,
            'requester': self.requester.to_dict() if self.requester else None,
            'owner_id': self.owner_id,
            'owner': self.owner.to_dict() if self.owner else None,
            'request_type': self.request_type,
            'status': self.status,
            'message': self.message,
            'rental_days': self.rental_days,
            'exchange_item_id': self.exchange_item_id,
            'requested_at': self.requested_at.isoformat(),
            'responded_at': self.responded_at.isoformat() if self.responded_at else None
        }
    
    def __repr__(self):
        return f'<Request {self.id} - {self.request_type}>'


# ============================================
# ORDER MODEL
# ============================================
class Order(db.Model):
    """
    Orders for completed transactions
    """
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('requests.id'), nullable=False, index=True)
    item_id = db.Column(db.Integer, db.ForeignKey('clothing_items.id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Transaction details
    order_type = db.Column(db.String(20), nullable=False)  # purchase, rental, exchange
    total_amount = db.Column(db.Float)
    commission = db.Column(db.Float, default=0)
    
    # Status
    status = db.Column(db.String(20), default='pending', index=True)  # pending, confirmed, shipped, delivered, returned, cancelled
    
    # Shipping details
    delivery_address = db.Column(db.Text, nullable=False)
    tracking_number = db.Column(db.String(50))
    
    # Timestamps
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    shipped_date = db.Column(db.DateTime)
    delivered_date = db.Column(db.DateTime)
    return_date = db.Column(db.DateTime)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'request_id': self.request_id,
            'item_id': self.item_id,
            'item': self.item.to_dict() if self.item else None,
            'buyer_id': self.buyer_id,
            'seller_id': self.seller_id,
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
    
    @property
    def item(self):
        """Get associated item"""
        return ClothingItem.query.get(self.item_id)


# ============================================
# IMPACT METRICS MODEL
# ============================================
class ImpactMetrics(db.Model):
    """
    Track sustainability impact of user actions
    """
    __tablename__ = 'impact_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    item_id = db.Column(db.Integer, db.ForeignKey('clothing_items.id'))
    
    # Action type
    action_type = db.Column(db.String(20), nullable=False)  # item_reworn, item_rented, item_sold, item_exchanged
    
    # Impact data
    co2_reduced_kg = db.Column(db.Float, nullable=False)
    water_saved_liters = db.Column(db.Float, nullable=False)
    textile_waste_prevented_kg = db.Column(db.Float, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'item_id': self.item_id,
            'action_type': self.action_type,
            'co2_reduced_kg': self.co2_reduced_kg,
            'water_saved_liters': self.water_saved_liters,
            'textile_waste_prevented_kg': self.textile_waste_prevented_kg,
            'created_at': self.created_at.isoformat()
        }


# ============================================
# REVIEW MODEL
# ============================================
class Review(db.Model):
    """
    User reviews and ratings
    """
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    reviewed_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    review_text = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    reviewer = db.relationship('User', foreign_keys=[reviewer_id], backref='reviews_given')
    reviewed = db.relationship('User', foreign_keys=[reviewed_user_id], backref='reviews_received')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'reviewer_id': self.reviewer_id,
            'reviewer': self.reviewer.to_dict() if self.reviewer else None,
            'rating': self.rating,
            'review_text': self.review_text,
            'created_at': self.created_at.isoformat()
        }


# ============================================
# WISHLIST MODEL
# ============================================
class Wishlist(db.Model):
    """
    User wishlists
    """
    __tablename__ = 'wishlist'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    item_id = db.Column(db.Integer, db.ForeignKey('clothing_items.id'), nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    item = db.relationship('ClothingItem', backref='wishlisted_by')
    
    __table_args__ = (db.UniqueConstraint('user_id', 'item_id', name='unique_wishlist'),)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'item_id': self.item_id,
            'item': self.item.to_dict() if self.item else None,
            'added_at': self.added_at.isoformat()
        }


# ============================================
# NOTIFICATION MODEL
# ============================================
class Notification(db.Model):
    """
    User notifications
    """
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    title = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.String(20), default='system')  # order, request, message, system
    is_read = db.Column(db.Boolean, default=False, index=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='notifications')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'message': self.message,
            'notification_type': self.notification_type,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat()
        }
