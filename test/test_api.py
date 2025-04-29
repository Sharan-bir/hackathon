import requests
import json
import os
from datetime import datetime
import random
import string

# Base URL for the API
BASE_URL = 'http://localhost:8000/api'

def generate_random_string(length=6):
    """Generate a random string for unique usernames"""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

# Test data
TEST_USER = {
    'username': f'test_user_{generate_random_string()}',
    'email': 'test_user@example.com',
    'password': 'testpass123',
    'phone': '1234567890',
    'address': 'Test Address',
    'user_type': 1
}

TEST_POLICE = {
    'username': f'test_police_{generate_random_string()}',
    'email': 'test_police@example.com',
    'password': 'testpass123',
    'police_id': 'POL123',
    'user_type': 2
}

TEST_DEPARTMENT = {
    'username': f'test_dept_{generate_random_string()}',
    'email': 'test_department@example.com',
    'password': 'testpass123',
    'user_type': 3
}

TEST_POLICE_STATION = {
    'name': f'Test Police Station {generate_random_string()}',
    'location': 'Test Station Address',
    'latitude': 27.7172,
    'longitude': 85.3240,
    'head': None  # Will be set after police user creation
}

TEST_CRIME_REPORT = {
    'description': 'This is a test crime report',
    'crime_type': 'theft',
    'address': 'Test Location',
    'latitude': 27.7172,
    'longitude': 85.3240
}

def test_create_crime_report(token):
    """Test crime report creation endpoint"""
    print("\nTesting Crime Report Creation...")
    headers = {'Authorization': f'Bearer {token}'}
    # Create multipart form data
    files = {}  # You can add an image file here if needed
    data = {
        'description': TEST_CRIME_REPORT['description'],
        'crime_type': TEST_CRIME_REPORT['crime_type'],
        'address': TEST_CRIME_REPORT['address'],
        'latitude': TEST_CRIME_REPORT['latitude'],
        'longitude': TEST_CRIME_REPORT['longitude']
    }
    response = requests.post(
        f'{BASE_URL}/crime-reports/',
        headers=headers,
        data=data,
        files=files
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json() if response.status_code == 201 else None 