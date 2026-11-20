from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from mongoengine import (
    Document,
    StringField,
    IntField,
    FloatField,
    BooleanField,
    DateTimeField,
    ReferenceField,
    DENY,
    PULL,
)


class User(Document):
    username = StringField(unique=True, required=True)
    email = StringField(unique=True, required=True)
    password_hash = StringField(required=True)
    full_name = StringField(required=True)
    mobile = StringField()
    address = StringField()
    profile_image_url = StringField()
    bio = StringField()
    role = StringField(choices=["user", "admin"], default="user")

    carbon_saved_kg = FloatField(default=0)
    water_saved_liters = FloatField(default=0)
    items_reworn = IntField(default=0)
    items_rented = IntField(default=0)
    items_sold = IntField(default=0)
    items_exchanged = IntField(default=0)
    reputation_score = IntField(default=0)

    is_active = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "users",
        "indexes": ["username", "email", "role", "is_active", "created_at"],
    }

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": str(self.id),
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "mobile": self.mobile,
            "address": self.address,
            "profile_image_url": self.profile_image_url,
            "bio": self.bio,
            "role": self.role,
            "is_active": self.is_active,
            "carbon_saved_kg": float(self.carbon_saved_kg or 0),
            "water_saved_liters": float(self.water_saved_liters or 0),
            "items_reworn": int(self.items_reworn or 0),
            "items_rented": int(self.items_rented or 0),
            "items_sold": int(self.items_sold or 0),
            "items_exchanged": int(self.items_exchanged or 0),
            "reputation_score": int(self.reputation_score or 0),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class ClothingItem(Document):
    owner = ReferenceField(User, required=True, reverse_delete_rule=DENY)

    title = StringField(required=True)
    description = StringField()
    category = StringField(required=True)
    size = StringField(required=True)
    color = StringField()
    brand = StringField()
    exchange_preferences = StringField()

    condition = StringField(required=True, choices=["new", "like_new", "good", "fair", "worn"])
    transaction_type = StringField(required=True, choices=["rent", "buy", "exchange", "free"])

    price = FloatField(default=0.0)
    rental_price_per_day = FloatField(default=0.0)
    image_url = StringField()

    status = StringField(
        default="available",
        choices=["available", "rented", "sold", "exchanged", "inactive"],
    )

    carbon_impact_kg = FloatField(default=0)
    water_impact_liters = FloatField(default=0)
    rewear_count = IntField(default=0)

    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "clothing_items",
        "indexes": ["owner", "status", "category", "transaction_type", "created_at"],
    }

    def to_dict(self):
        return {
            "id": str(self.id),
            "owner_id": str(self.owner.id) if self.owner else None,
            "owner": {
                "id": str(self.owner.id),
                "username": self.owner.username,
                "full_name": self.owner.full_name,
            }
            if self.owner
            else None,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "size": self.size,
            "color": self.color,
            "brand": self.brand,
            "exchange_preferences": self.exchange_preferences,
            "condition": self.condition,
            "transaction_type": self.transaction_type,
            "price": float(self.price or 0),
            "rental_price_per_day": float(self.rental_price_per_day or 0),
            "image_url": self.image_url or "https://via.placeholder.com/300",
            "status": self.status,
            "carbon_impact_kg": float(self.carbon_impact_kg or 0),
            "water_impact_liters": float(self.water_impact_liters or 0),
            "rewear_count": int(self.rewear_count or 0),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class Request(Document):
    item = ReferenceField(ClothingItem, required=True, reverse_delete_rule=DENY)
    requester = ReferenceField(User, required=True, reverse_delete_rule=DENY)
    owner = ReferenceField(User, required=True, reverse_delete_rule=DENY)

    request_type = StringField(required=True, choices=["rent", "buy", "exchange", "gift"])
    status = StringField(default="pending", choices=["pending", "accepted", "rejected", "cancelled", "completed"])

    message = StringField()
    rental_days = IntField()
    exchange_item = ReferenceField(ClothingItem, reverse_delete_rule=PULL)

    requested_at = DateTimeField(default=datetime.utcnow)
    responded_at = DateTimeField()
    completed_at = DateTimeField()

    meta = {
        "collection": "requests",
        "indexes": ["item", "requester", "owner", "status", "request_type", "requested_at"],
    }

    def to_dict(self):
        return {
            "id": str(self.id),
            "item_id": str(self.item.id) if self.item else None,
            "item": self.item.to_dict() if self.item else None,
            "requester_id": str(self.requester.id) if self.requester else None,
            "requester": self.requester.to_dict() if self.requester else None,
            "owner_id": str(self.owner.id) if self.owner else None,
            "owner": self.owner.to_dict() if self.owner else None,
            "request_type": self.request_type,
            "status": self.status,
            "message": self.message,
            "rental_days": self.rental_days,
            "exchange_item_id": str(self.exchange_item.id) if self.exchange_item else None,
            "exchange_item": self.exchange_item.to_dict() if self.exchange_item else None,
            "requested_at": self.requested_at.isoformat() if self.requested_at else None,
            "responded_at": self.responded_at.isoformat() if self.responded_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }


class Order(Document):
    request = ReferenceField(Request, required=True, reverse_delete_rule=DENY)
    item = ReferenceField(ClothingItem, required=True, reverse_delete_rule=DENY)
    buyer = ReferenceField(User, required=True, reverse_delete_rule=DENY)
    seller = ReferenceField(User, required=True, reverse_delete_rule=DENY)

    order_type = StringField(required=True, choices=["purchase", "rental", "exchange"])
    total_amount = FloatField(default=0)
    commission = FloatField(default=0)

    status = StringField(
        default="pending",
        choices=["pending", "confirmed", "shipped", "delivered", "returned", "cancelled"],
    )

    delivery_address = StringField(required=True)
    tracking_number = StringField()

    order_date = DateTimeField(default=datetime.utcnow)
    shipped_date = DateTimeField()
    delivered_date = DateTimeField()
    return_date = DateTimeField()

    meta = {
        "collection": "orders",
        "indexes": ["buyer", "seller", "status", "order_date"],
    }

    def to_dict(self):
        return {
            "id": str(self.id),
            "request_id": str(self.request.id) if self.request else None,
            "item_id": str(self.item.id) if self.item else None,
            "item": self.item.to_dict() if self.item else None,
            "buyer_id": str(self.buyer.id) if self.buyer else None,
            "seller_id": str(self.seller.id) if self.seller else None,
            "order_type": self.order_type,
            "total_amount": float(self.total_amount or 0),
            "commission": float(self.commission or 0),
            "status": self.status,
            "delivery_address": self.delivery_address,
            "tracking_number": self.tracking_number,
            "order_date": self.order_date.isoformat() if self.order_date else None,
            "shipped_date": self.shipped_date.isoformat() if self.shipped_date else None,
            "delivered_date": self.delivered_date.isoformat() if self.delivered_date else None,
            "return_date": self.return_date.isoformat() if self.return_date else None,
        }


class ImpactMetrics(Document):
    user = ReferenceField(User, required=True, reverse_delete_rule=DENY)
    item = ReferenceField(ClothingItem, reverse_delete_rule=PULL)

    action_type = StringField(required=True, choices=["item_reworn", "item_rented", "item_sold", "item_exchanged"])
    co2_reduced_kg = FloatField(required=True)
    water_saved_liters = FloatField(required=True)
    textile_waste_prevented_kg = FloatField(default=0)

    created_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "impact_metrics",
        "indexes": ["user", "action_type", "created_at"],
    }

    def to_dict(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user.id) if self.user else None,
            "item_id": str(self.item.id) if self.item else None,
            "action_type": self.action_type,
            "co2_reduced_kg": float(self.co2_reduced_kg or 0),
            "water_saved_liters": float(self.water_saved_liters or 0),
            "textile_waste_prevented_kg": float(self.textile_waste_prevented_kg or 0),
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Wishlist(Document):
    user = ReferenceField(User, required=True, reverse_delete_rule=DENY)
    item = ReferenceField(ClothingItem, required=True, reverse_delete_rule=DENY)
    added_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "wishlist",
        "indexes": [("user", "item"), "user"],
    }


class Review(Document):
    reviewer = ReferenceField(User, required=True, reverse_delete_rule=DENY)
    reviewed_user = ReferenceField(User, required=True, reverse_delete_rule=DENY)
    order = ReferenceField(Order)
    rating = IntField(required=True, min_value=1, max_value=5)
    review_text = StringField()
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "reviews",
        "indexes": ["reviewer", "reviewed_user", "created_at"],
    }


class Notification(Document):
    user = ReferenceField(User, required=True, reverse_delete_rule=DENY)
    title = StringField(required=True)
    message = StringField(required=True)
    notification_type = StringField(default="system", choices=["order", "request", "message", "system"])
    is_read = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "notifications",
        "indexes": ["user", "is_read", "created_at"],
    }


class Message(Document):
    sender = ReferenceField(User, required=True, reverse_delete_rule=DENY)
    receiver = ReferenceField(User, required=True, reverse_delete_rule=DENY)
    item = ReferenceField(ClothingItem, reverse_delete_rule=PULL)
    content = StringField(required=True)
    timestamp = DateTimeField(default=datetime.utcnow)
    is_read = BooleanField(default=False)

    meta = {
        "collection": "messages",
        "indexes": ["sender", "receiver", "timestamp"],
    }

    def to_dict(self):
        return {
            "id": str(self.id),
            "sender_id": str(self.sender.id) if self.sender else None,
            "receiver_id": str(self.receiver.id) if self.receiver else None,
            "item_id": str(self.item.id) if self.item else None,
            "content": self.content,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "is_read": self.is_read,
        }
