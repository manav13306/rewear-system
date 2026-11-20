from flask import Blueprint, request, jsonify
from models.models import Message, User, ClothingItem
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from mongoengine.errors import ValidationError

messages_bp = Blueprint('messages', __name__)

# 1. Send a Message
@messages_bp.route('', methods=['POST'])
@jwt_required()
def send_message():
    current_user_id = get_jwt_identity()
    data = request.get_json()

    if not data or 'receiver_id' not in data or 'content' not in data:
        return jsonify({"msg": "Missing receiver or content"}), 400

    try:
        # Create new Message document
        new_msg = Message(
            sender=current_user_id,
            receiver=data['receiver_id'],
            item=data.get('item_id'), # ReferenceField handles the ID
            content=data['content'],
            timestamp=datetime.utcnow()
        )

        new_msg.save() # MongoEngine save method

        return jsonify({"msg": "Message sent successfully", "message": new_msg.to_dict()}), 201
    
    except ValidationError as e:
        return jsonify({"msg": "Invalid ID format", "error": str(e)}), 400
    except Exception as e:
        return jsonify({"msg": "Server Error", "error": str(e)}), 500

# 2. Get Chat History with a specific user
@messages_bp.route('/history/<string:other_user_id>', methods=['GET']) # Changed <int> to <string>
@jwt_required()
def get_chat_history(other_user_id):
    current_user_id = get_jwt_identity()

    # Fetch messages where (Me -> Them) OR (Them -> Me)
    # Using MongoEngine Q objects for complex OR queries
    from mongoengine import Q
    
    messages = Message.objects(
        (Q(sender=current_user_id) & Q(receiver=other_user_id)) |
        (Q(sender=other_user_id) & Q(receiver=current_user_id))
    ).order_by('timestamp')

    return jsonify([m.to_dict() for m in messages]), 200

# 3. Get Inbox (List of people I've talked to)
@messages_bp.route('/inbox', methods=['GET'])
@jwt_required()
def get_inbox():
    current_user_id = get_jwt_identity()
    
    # Find all unique IDs involved in conversations with the current user
    sent_to = Message.objects(sender=current_user_id).distinct('receiver')
    received_from = Message.objects(receiver=current_user_id).distinct('sender')
    
    # Combine and get unique user IDs (using sets to handle string IDs)
    contact_ids = list(set([str(uid.id) for uid in sent_to] + [str(uid.id) for uid in received_from]))

    # Fetch User objects for these IDs
    contacts = User.objects(id__in=contact_ids)
    
    return jsonify([{
        "id": str(user.id),
        "username": user.username,
        "full_name": user.full_name
    } for user in contacts]), 200