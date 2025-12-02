#!/usr/bin/env python3
"""
Script to create an admin user for testing admin functionality
"""
import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.user import User

def create_admin_user():
    app = create_app()
    
    with app.app_context():
        # Check if admin user already exists
        admin_user = User.query.filter_by(username='admin').first()
        
        if admin_user:
            print("Admin user already exists!")
            print(f"Username: {admin_user.username}")
            print(f"Email: {admin_user.email}")
            print(f"Role: {admin_user.role}")
            return
        
        # Create admin user
        admin = User(
            username='admin',
            email='admin@bank.com',
            password='Admin123!'
        )
        admin.first_name = 'Admin'
        admin.last_name = 'User'
        admin.role = 'admin'
        
        db.session.add(admin)
        db.session.commit()
        
        print("Admin user created successfully!")
        print("Username: admin")
        print("Email: admin@bank.com")
        print("Password: Admin123!")
        print("Role: admin")

if __name__ == '__main__':
    create_admin_user()