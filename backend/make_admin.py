import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
from models.models import User

app = create_app()
with app.app_context():
    email = "admin@rewear.com"
    user = User.objects(email=email).first()
    
    if not user:
        print(f"User {email} not found. Creating admin user...")
        user = User(
            username="admin_rewear",
            email=email,
            full_name="Admin ReWear",
            role="admin",
            is_active=True
        )
        user.set_password("Admin123!")
        user.save()
        print(f"Created admin user with password: Admin123!")
    else:
        print(f"Found user: {user.username}, role: {user.role}")
        if user.role != 'admin':
            user.role = 'admin'
            print("Updated role to admin")
        user.set_password("Admin123!")
        user.save()
        print(f"Password reset to: Admin123!")
    
    print(f"\nUser Details:")
    print(f"  Username: {user.username}")
    print(f"  Email: {user.email}")
    print(f"  Role: {user.role}")
    print(f"  Active: {user.is_active}")
    print(f"\nLogin with: admin@rewear.com / Admin123!")
