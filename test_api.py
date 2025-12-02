#!/usr/bin/env python3
"""
Test script to identify potential API issues
"""
import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_api_endpoints():
    """Test all main API endpoints to identify issues"""
    
    print("Testing API endpoints...")
    
    # Test home endpoint
    print("\n1. Testing home endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test user registration
    print("\n2. Testing user registration...")
    user_data = {
        "username": "testuser",
        "email": "test@example.com", 
        "password": "Test123!",
        "first_name": "Test",
        "last_name": "User"
    }
    try:
        response = requests.post(f"{BASE_URL}/api/auth/register", json=user_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200 or response.status_code == 201:
            print(f"   Response: {response.json()}")
        else:
            print(f"   Error Response: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test user login
    print("\n3. Testing user login...")
    login_data = {
        "email": "test@example.com",
        "password": "Test123!"
    }
    try:
        response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Login successful: {result.get('message')}")
            token = result.get('access_token') or result.get('token')
            if token:
                print(f"   Token received: {token[:50]}...")
                return token
        else:
            print(f"   Login failed: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    return None

def test_with_token(token):
    """Test endpoints that require authentication"""
    if not token:
        print("No token available, skipping authenticated tests")
        return
        
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test profile endpoint
    print("\n4. Testing profile endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/auth/profile", headers=headers)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test account creation
    print("\n5. Testing account creation...")
    account_data = {
        "account_type": "checking",
        "account_name": "Test Account",
        "initial_balance": 100.0
    }
    try:
        response = requests.post(f"{BASE_URL}/api/accounts", json=account_data, headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            result = response.json()
            print(f"   Account created: {result}")
            return result.get('id')
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    return None

def main():
    print("Starting API tests...")
    
    # Wait a moment for server to be ready
    time.sleep(2)
    
    token = test_api_endpoints()
    account_id = test_with_token(token)
    
    print("\n" + "="*50)
    print("API test completed!")

if __name__ == "__main__":
    main()