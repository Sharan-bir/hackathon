import requests
import json
import os
from datetime import datetime
import random
import string

# Base URL for the API
BASE_URL = 'http://127.0.0.1:8000/api'

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

TEST_POLICEMAN = {
    'username': f'test_policeman_{generate_random_string()}',
    'password': 'testpass123',
    'email': 'test_policeman@example.com',
    'police_id': 'POL456',
    'phone': '9876543210',
    'address': 'Test Policeman Address'
}

TEST_POLICE_TEAM = {
    'name': f'Test Team {generate_random_string()}',
    'members': []  # Will be populated with policeman IDs
}

def test_user_registration():
    """Test user registration endpoint"""
    print("\nTesting User Registration...")
    response = requests.post(f'{BASE_URL}/register/', json=TEST_USER)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json() if response.status_code == 201 else None

def test_police_registration():
    """Test police registration endpoint"""
    print("\nTesting Police Registration...")
    response = requests.post(f'{BASE_URL}/register/', json=TEST_POLICE)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json() if response.status_code == 201 else None

def test_department_registration():
    """Test department registration endpoint"""
    print("\nTesting Department Registration...")
    response = requests.post(f'{BASE_URL}/register/', json=TEST_DEPARTMENT)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json() if response.status_code == 201 else None

def test_login(username, password):
    """Test login endpoint"""
    print(f"\nTesting Login for {username}...")
    response = requests.post(f'{BASE_URL}/login/', json={
        'username': username,
        'password': password
    })
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json() if response.status_code == 200 else None

def test_create_police_station(token, head_id):
    """Test police station creation endpoint"""
    print("\nTesting Police Station Creation...")
    TEST_POLICE_STATION['head'] = head_id
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(f'{BASE_URL}/police-stations/', json=TEST_POLICE_STATION, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json() if response.status_code == 201 else None

def test_create_crime_report(token):
    """Test crime report creation endpoint"""
    print("\nTesting Crime Report Creation...")
    headers = {'Authorization': f'Bearer {token}'}
    # Create multipart form data
    data = {
        'description': TEST_CRIME_REPORT['description'],
        'crime_type': TEST_CRIME_REPORT['crime_type'],
        'address': TEST_CRIME_REPORT['address'],
        'latitude': TEST_CRIME_REPORT['latitude'],
        'longitude': TEST_CRIME_REPORT['longitude']
    }
    files = {}  # You can add an image file here if needed
    response = requests.post(
        f'{BASE_URL}/crime-reports/',
        headers=headers,
        data=data,
        files=files
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json() if response.status_code == 201 else None

def test_get_recent_reports(token):
    """Test getting recent reports endpoint"""
    print("\nTesting Get Recent Reports...")
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{BASE_URL}/recent-reports/', headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json() if response.status_code == 200 else None

def test_update_report_status(token, report_id):
    """Test updating report status endpoint"""
    print("\nTesting Update Report Status...")
    headers = {'Authorization': f'Bearer {token}'}
    data = {
        'status': 'under_progress',
        'police_notes': 'Investigation started'
    }
    response = requests.patch(
        f'{BASE_URL}/crime-reports/{report_id}/update-status/',
        json=data,
        headers=headers
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json() if response.status_code == 200 else None

def test_get_crime_stats(token):
    """Test getting crime statistics endpoint"""
    print("\nTesting Get Crime Statistics...")
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{BASE_URL}/crime-stats/', headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json() if response.status_code == 200 else None

def test_get_dashboard(token):
    """Test getting dashboard data endpoint"""
    print("\nTesting Get Dashboard Data...")
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{BASE_URL}/dashboard/', headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json() if response.status_code == 200 else None

def test_manage_policemen(token):
    """Test managing policemen in a police station"""
    print("\nTesting Policeman Management...")
    headers = {'Authorization': f'Bearer {token}'}
    
    # Add a policeman
    print("Adding policeman...")
    response = requests.post(
        f'{BASE_URL}/manage-policemen/',
        headers=headers,
        json=TEST_POLICEMAN
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 201:
        # List policemen
        print("\nListing policemen...")
        response = requests.get(
            f'{BASE_URL}/manage-policemen/',
            headers=headers
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Remove policeman
        print("\nRemoving policeman...")
        response = requests.delete(
            f'{BASE_URL}/manage-policemen/{TEST_POLICEMAN["username"]}/',
            headers=headers
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    
    return response.status_code in [200, 201]

def test_manage_police_team(token, station_id):
    """Test managing police teams"""
    print("\nTesting Police Team Management...")
    headers = {'Authorization': f'Bearer {token}'}
    
    # Create a team
    print("Creating team...")
    team_data = {
        'name': f'Test Team {generate_random_string()}',
        'members': [],
        'station': station_id
    }
    response = requests.post(
        f'{BASE_URL}/police-teams/',
        headers=headers,
        json=team_data
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 201:
        team_id = response.json()['id']
        
        # Get policeman ID
        print("\nGetting policeman ID...")
        response = requests.get(
            f'{BASE_URL}/manage-policemen/',
            headers=headers
        )
        if response.status_code == 200 and response.json():
            policeman_id = response.json()[0]['id']
            
            # Add members to team
            print("\nAdding members to team...")
            response = requests.patch(
                f'{BASE_URL}/police-teams/{team_id}/',
                headers=headers,
                json={'members': [policeman_id]}
            )
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.json()}")
            
            # Assign report to team
            print("\nAssigning report to team...")
            response = requests.post(
                f'{BASE_URL}/assign-report/',
                headers=headers,
                json={
                    'report': 1,  # Assuming report ID 1 exists
                    'team': team_id
                }
            )
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.json()}")
    
    return response.status_code in [200, 201]

def main():
    """Main function to run all tests"""
    print("Starting API Tests...")
    
    # Test user registration and login
    user_data = test_user_registration()
    if user_data:
        user_token = test_login(TEST_USER['username'], TEST_USER['password'])
        if user_token:
            user_token = user_token['access']
            # Test creating crime report as user
            report_data = test_create_crime_report(user_token)
            # Test getting dashboard data as user
            test_get_dashboard(user_token)
    
    # Test department registration and login first
    department_data = test_department_registration()
    if department_data:
        department_token = test_login(TEST_DEPARTMENT['username'], TEST_DEPARTMENT['password'])
        if department_token:
            department_token = department_token['access']
            # Test getting recent reports
            test_get_recent_reports(department_token)
            # Test getting crime statistics
            test_get_crime_stats(department_token)
            # Test getting dashboard data as department
            test_get_dashboard(department_token)
    
    # Test police registration and login
    police_data = test_police_registration()
    if police_data:
        police_token = test_login(TEST_POLICE['username'], TEST_POLICE['password'])
        if police_token and department_token:
            police_token = police_token['access']
            # Create police station using department token
            station_data = test_create_police_station(department_token, police_data['id'])
            
            if station_data:
                # Test managing policemen
                test_manage_policemen(police_token)
                # Test managing police teams
                test_manage_police_team(police_token, station_data['id'])
            
            # If we have a report ID and station is created, test updating its status
            if 'report_data' in locals() and report_data and station_data:
                test_update_report_status(police_token, report_data['id'])
                # Test getting dashboard data as police
                test_get_dashboard(police_token)

if __name__ == '__main__':
    main() 