# Crime Reporting System API Documentation

## Overview
The Crime Reporting System is a comprehensive API that enables citizens to report crimes, police departments to manage reports, and administrators to oversee the entire system. The system supports user management, crime reporting, police station management, and team assignments.

## Authentication
The system uses JWT (JSON Web Token) authentication. All authenticated endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <access_token>
```

## User Types
1. Regular User (user_type: 1)
2. Police Officer (user_type: 2)
3. Department Admin (user_type: 3)

## API Endpoints

### 1. User Management

#### Register User
- **URL**: `/api/register/`
- **Method**: POST
- **Access**: Public
- **Request Body**:
```json
{
    "username": "username",
    "email": "user@example.com",
    "password": "password123",
    "phone": "1234567890",
    "address": "User Address",
    "user_type": 1
}
```
Additional fields for police registration:
```json
{
    "username": "police_officer",
    "email": "police@example.com",
    "password": "password123",
    "police_id": "POL123",
    "user_type": 2
}
```

#### Login
- **URL**: `/api/login/`
- **Method**: POST
- **Access**: Public
- **Request Body**:
```json
{
    "username": "username",
    "password": "password123"
}
```
- **Response**:
```json
{
    "refresh": "refresh_token",
    "access": "access_token",
    "user_type": 1,
    "username": "username"
}
```

### 2. Crime Reports

#### Create Crime Report
- **URL**: `/api/crime-reports/`
- **Method**: POST
- **Access**: Authenticated Users
- **Request Body** (multipart/form-data):
```json
{
    "description": "Crime description",
    "crime_type": "theft",
    "address": "Crime Location",
    "latitude": "27.7172",
    "longitude": "85.3240",
    "image": "(optional) image file"
}
```

#### Get Recent Reports
- **URL**: `/api/recent-reports/`
- **Method**: GET
- **Access**: Police & Department
- **Response**: List of 5 most recent crime reports

#### Update Report Status
- **URL**: `/api/crime-reports/{id}/update-status/`
- **Method**: PATCH
- **Access**: Station Head
- **Request Body**:
```json
{
    "status": "under_progress",
    "police_notes": "Investigation notes"
}
```

### 3. Police Station Management

#### Create Police Station
- **URL**: `/api/police-stations/`
- **Method**: POST
- **Access**: Department Admin
- **Request Body**:
```json
{
    "name": "Station Name",
    "location": "Station Address",
    "latitude": "27.7172",
    "longitude": "85.3240",
    "head": "police_user_id"
}
```

### 4. Police Team Management

#### Create Police Team
- **URL**: `/api/police-teams/`
- **Method**: POST
- **Access**: Station Head
- **Request Body**:
```json
{
    "name": "Team Name",
    "members": ["policeman_id1", "policeman_id2"],
    "station": "station_id"
}
```

#### Manage Policemen
- **URL**: `/api/manage-policemen/`
- **Method**: POST
- **Access**: Station Head
- **Request Body**:
```json
{
    "username": "policeman_username",
    "password": "password123",
    "email": "policeman@example.com",
    "police_id": "POL456",
    "phone": "9876543210",
    "address": "Policeman Address"
}
```

### 5. Report Assignment

#### Assign Report to Team
- **URL**: `/api/assign-report/`
- **Method**: POST
- **Access**: Station Head
- **Request Body**:
```json
{
    "report": "report_id",
    "team": "team_id"
}
```

### 6. Statistics and Dashboard

#### Crime Statistics
- **URL**: `/api/crime-stats/`
- **Method**: GET
- **Access**: Department Admin
- **Response**:
```json
{
    "crime_types": [
        {"crime_type": "theft", "count": 10}
    ],
    "hotspots": [
        {"address": "Location", "count": 5}
    ],
    "status_distribution": [
        {"status": "pending", "count": 3},
        {"status": "under_progress", "count": 7}
    ]
}
```

#### Dashboard
- **URL**: `/api/dashboard/`
- **Method**: GET
- **Access**: Authenticated Users
- **Response** (varies by user type):
```json
{
    "crime_types": [],
    "status_distribution": [],
    "station_reports": [],
    "recent_reports": [],
    "total_reports": 0,
    "active_reports": 0
}
```

## Key Features

1. **User Management**
   - User registration with different roles
   - Secure JWT authentication
   - Role-based access control

2. **Crime Reporting**
   - Submit crime reports with location and media
   - Track report status
   - View report history

3. **Police Station Management**
   - Create and manage police stations
   - Assign station heads
   - Monitor station performance

4. **Team Management**
   - Create police teams
   - Assign officers to teams
   - Manage team assignments

5. **Report Assignment**
   - Assign reports to police teams
   - Track investigation progress
   - Update report status

6. **Analytics and Dashboard**
   - Crime statistics by type and location
   - Station-wise performance metrics
   - Status distribution analysis
   - Recent activity monitoring

## Testing
All endpoints have been thoroughly tested with the test suite in `test_api.py`. The tests cover:
- User registration and authentication
- Crime report creation and management
- Police station and team operations
- Report assignments and status updates
- Dashboard and statistics retrieval 