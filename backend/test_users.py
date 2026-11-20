#!/usr/bin/env python3

from database import init_mongodb
from app import create_app
from models.models import User

# Initialize app and database
app = create_app()
app.app_context().push()

# Test user login
user = User.objects(email='test@example.com').first()
if user:
    print(f"User found: {user.username}")
    print(f"Password hash exists: {bool(user.password_hash)}")
    print(f"Password check 'Password123': {user.check_password('Password123')}")
    print(f"Password check 'password123': {user.check_password('password123')}")
else:
    print("User not found")

# Show all users
print("\nAll users:")
for u in User.objects():
    print(f"- {u.username}: {u.email} (active: {u.is_active})")