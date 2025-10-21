# Assignment Management System

A comprehensive Django REST Framework-based assignment management system for educational institutions, featuring JWT authentication, PostgreSQL database, and RESTful API endpoints.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Database Schema](#database-schema)
- [Installation](#installation)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Authentication](#authentication)
- [Usage Examples](#usage-examples)
- [Project Structure](#project-structure)
- [Development](#development)
- [Troubleshooting](#troubleshooting)

---

## Overview

The Assignment Management System is a backend application designed to manage educational assignments, students, courses, and submissions. It provides a robust REST API for creating, retrieving, and managing assignments with support for multiple courses, semesters, subjects, and technical skills.

### Key Capabilities
- User authentication and authorization using JWT tokens
- Organization and course management
- Student registration and management
- Assignment creation with multiple tech skills
- Assignment submission tracking with marks and remarks
- PostgreSQL database for reliable data storage

---

## Features

### Core Features
- **JWT Authentication**: Secure token-based authentication using `djangorestframework-simplejwt`
- **Master Data Management**:
  - Organizations
  - Courses
  - Semesters
  - Subjects
  - Technical Skills
- **Student Management**: Track students with USN numbers, emails, and course enrollments
- **Assignment Management**:
  - Create assignments with detailed descriptions
  - Set start and end dates
  - Define total marks
  - Associate multiple technical skills
  - Link to courses, semesters, and subjects
- **Assignment Submission Tracking**:
  - Record student submissions
  - Store obtained marks
  - Add remarks and feedback
  - Track submission dates

### Technical Features
- UUID-based primary keys for enhanced security
- RESTful API design
- PostgreSQL database backend
- Django ORM for database operations
- Serializer validation
- Nested serializers for complex relationships
- Many-to-many relationship support

---

## Technology Stack

### Backend Framework
- **Django**: 5.2.7
- **Django REST Framework**: 3.16.1
- **Django REST Framework SimpleJWT**: 5.5.1

### Database
- **PostgreSQL**: Database engine
- **psycopg2-binary**: 2.9.11 (PostgreSQL adapter)

### Authentication
- **PyJWT**: 2.10.1 (JSON Web Token implementation)

### Additional Dependencies
- **asgiref**: 3.10.0 (ASGI server reference)
- **sqlparse**: 0.5.3 (SQL parsing)
- **tzdata**: 2025.2 (Timezone data)

### Development Environment
- **Python**: 3.x (Virtual environment: `env/`)
- **Windows**: PowerShell compatible

---

## Database Schema

### Master Tables

#### User (Extends AbstractUser)
Custom user model for authentication and authorization.
- Inherits all fields from Django's AbstractUser
- Username, email, password, first_name, last_name, etc.
- Can be extended with professor-specific fields

#### Org (Organization)
```python
- id: UUID (Primary Key)
- name: CharField(100, unique)
```

#### Course
```python
- id: UUID (Primary Key)
- course_name: CharField(100, unique)
- course_code: CharField(20, unique)
- org: ForeignKey(Org)
```

#### Semester
```python
- id: UUID (Primary Key)
- semester_name: CharField(50, unique)
- sem_code: CharField(20, unique)
```

#### Subject
```python
- id: UUID (Primary Key)
- subject_name: CharField(100, unique)
- subject_code: CharField(20, unique)
```

#### TechSkill (Technical Skill)
```python
- id: UUID (Primary Key)
- skill_name: CharField(50, unique)
- skill_code: CharField(20, unique)
```

### Transactional Tables

#### Student
```python
- id: UUID (Primary Key)
- student_usn_no: CharField(50, unique)
- email: EmailField(unique)
- gender: CharField(10)
- course: ForeignKey(Course)
```

#### Assignment
```python
- id: UUID (Primary Key)
- assignment_name: CharField(200)
- assignment_description: TextField(500)
- start_date: DateTimeField
- submission_end_date: DateTimeField
- total_marks: IntegerField
- assignment_code: CharField(20, unique)
- course: ForeignKey(Course)
- semester: ForeignKey(Semester)
- subject: ForeignKey(Subject)
- tech_skills: ManyToManyField(TechSkill)
```

#### AssignmentTransaction
```python
- id: UUID (Primary Key)
- obtained_marks: IntegerField
- candidate_submit_date: DateTimeField(auto_now_add)
- remarks: TextField
- student: ForeignKey(Student)
- assignment: ForeignKey(Assignment)
```

### Entity Relationships

```
Org (1) -----> (N) Course
Course (1) ---> (N) Student
Course (1) ---> (N) Assignment
Semester (1) -> (N) Assignment
Subject (1) --> (N) Assignment
TechSkill (N) <----> (N) Assignment (Many-to-Many)
Student (1) --> (N) AssignmentTransaction
Assignment (1) -> (N) AssignmentTransaction
```

---

## Installation

### Prerequisites
- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)

### Step 1: Clone the Repository
```powershell
git clone <repository-url>
cd assignment-management-system
```

### Step 2: Set Up PostgreSQL Database

1. Install PostgreSQL if not already installed
2. Open pgAdmin or use PostgreSQL command line
3. Create a new database:
```sql
CREATE DATABASE fsd_assignment;
```

4. Create a user (optional, or use the default `postgres` user):
```sql
CREATE USER your_username WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE fsd_assignment TO your_username;
```

### Step 3: Create Virtual Environment
```powershell
cd backend
python -m venv env
```

### Step 4: Activate Virtual Environment
```powershell
.\env\Scripts\Activate.ps1
```

If you encounter execution policy errors, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 5: Install Dependencies
```powershell
pip install django==5.2.7
pip install djangorestframework==3.16.1
pip install djangorestframework-simplejwt==5.5.1
pip install psycopg2-binary==2.9.11
```

Or if there's a `requirements.txt`:
```powershell
pip install -r requirements.txt
```

### Step 6: Apply Migrations
```powershell
python manage.py makemigrations
python manage.py migrate
```

### Step 7: Create Superuser
```powershell
python manage.py createsuperuser
```
Follow the prompts to create an admin user.

### Step 8: Run Development Server
```powershell
python manage.py runserver
```

The API will be available at: `http://127.0.0.1:8000/`

---

## Configuration

### Database Configuration

Edit `backend/core/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'fsd_assignment',  # Your database name
        'USER': 'postgres',         # Your PostgreSQL username
        'PASSWORD': 'password',     # Your PostgreSQL password
        'HOST': 'localhost',        # Database host
        'PORT': '5432',             # PostgreSQL port
    }
}
```

### JWT Configuration

The project uses default JWT settings. To customize, add to `settings.py`:

```python
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```

### Security Settings

**Important**: Before deploying to production:

1. Change the `SECRET_KEY` in `settings.py`
2. Set `DEBUG = False`
3. Configure `ALLOWED_HOSTS`:
```python
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
```

---

## API Documentation

### Base URL
```
http://127.0.0.1:8000/api/
```

### Authentication Endpoints

#### 1. Obtain JWT Token (Login)
**Endpoint**: `POST /api/token/`

**Description**: Authenticate user and receive access and refresh tokens.

**Request Body**:
```json
{
    "username": "your_username",
    "password": "your_password"
}
```

**Response** (200 OK):
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**cURL Example**:
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

#### 2. Refresh JWT Token
**Endpoint**: `POST /api/token/refresh/`

**Description**: Obtain a new access token using the refresh token.

**Request Body**:
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response** (200 OK):
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

### Master Data Endpoints

All endpoints below require JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer <access_token>
```

#### 3. Organizations

##### List/Create Organizations
**Endpoint**: `GET/POST /api/orgs/`

**GET Response**:
```json
[
    {
        "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "name": "ABC University"
    }
]
```

**POST Request Body**:
```json
{
    "name": "XYZ College"
}
```

**POST Response** (201 Created):
```json
{
    "id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
    "name": "XYZ College"
}
```

#### 4. Courses

##### List/Create Courses
**Endpoint**: `GET/POST /api/courses/`

**GET Response**:
```json
[
    {
        "id": "c3d4e5f6-a7b8-9012-cdef-123456789012",
        "course_name": "Computer Science Engineering",
        "course_code": "CSE",
        "org": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
    }
]
```

**POST Request Body**:
```json
{
    "course_name": "Information Science Engineering",
    "course_code": "ISE",
    "org": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

**Validation Rules**:
- `course_name`: Must be unique
- `course_code`: Must be unique
- `org`: Must be a valid UUID of an existing organization

#### 5. Semesters

##### List/Create Semesters
**Endpoint**: `GET/POST /api/semesters/`

**GET Response**:
```json
[
    {
        "id": "d4e5f6a7-b8c9-0123-def1-234567890123",
        "semester_name": "Fifth Semester",
        "sem_code": "SEM5"
    }
]
```

**POST Request Body**:
```json
{
    "semester_name": "Sixth Semester",
    "sem_code": "SEM6"
}
```

#### 6. Subjects

##### List/Create Subjects
**Endpoint**: `GET/POST /api/subjects/`

**GET Response**:
```json
[
    {
        "id": "e5f6a7b8-c9d0-1234-ef12-345678901234",
        "subject_name": "Full Stack Development",
        "subject_code": "FSD"
    }
]
```

**POST Request Body**:
```json
{
    "subject_name": "Machine Learning",
    "subject_code": "ML"
}
```

#### 7. Technical Skills

##### List/Create Technical Skills
**Endpoint**: `GET/POST /api/tech-skills/`

**GET Response**:
```json
[
    {
        "id": "f6a7b8c9-d0e1-2345-f123-456789012345",
        "skill_name": "Django",
        "skill_code": "DJANGO"
    }
]
```

**POST Request Body**:
```json
{
    "skill_name": "React",
    "skill_code": "REACT"
}
```

---

### Transactional Data Endpoints

#### 8. Students

##### List/Create Students
**Endpoint**: `GET/POST /api/students/`

**GET Response** (With nested course details):
```json
[
    {
        "id": "a7b8c9d0-e1f2-3456-1234-567890123456",
        "student_usn_no": "1MS21CS001",
        "email": "student@example.com",
        "gender": "Male",
        "course": {
            "id": "c3d4e5f6-a7b8-9012-cdef-123456789012",
            "course_name": "Computer Science Engineering",
            "course_code": "CSE",
            "org": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
        }
    }
]
```

**POST Request Body**:
```json
{
    "student_usn_no": "1MS21CS002",
    "email": "student2@example.com",
    "gender": "Female",
    "course_id": "c3d4e5f6-a7b8-9012-cdef-123456789012"
}
```

**POST Response** (201 Created):
```json
{
    "id": "b8c9d0e1-f2a3-4567-2345-678901234567",
    "student_usn_no": "1MS21CS002",
    "email": "student2@example.com",
    "gender": "Female",
    "course": {
        "id": "c3d4e5f6-a7b8-9012-cdef-123456789012",
        "course_name": "Computer Science Engineering",
        "course_code": "CSE",
        "org": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
    }
}
```

**Validation Rules**:
- `student_usn_no`: Must be unique
- `email`: Must be unique and valid email format
- `gender`: String field (e.g., "Male", "Female", "Other")
- `course_id`: Must be a valid UUID of an existing course

#### 9. Assignments

##### List/Create Assignments
**Endpoint**: `GET/POST /api/assignments/`

**GET Response** (With nested relationships):
```json
[
    {
        "id": "c9d0e1f2-a3b4-5678-3456-789012345678",
        "assignment_name": "REST API Development",
        "assignment_description": "Create a RESTful API using Django REST Framework",
        "start_date": "2025-10-15T10:00:00Z",
        "submission_end_date": "2025-10-30T23:59:59Z",
        "total_marks": 100,
        "assignment_code": "FSD_A1",
        "course": {
            "id": "c3d4e5f6-a7b8-9012-cdef-123456789012",
            "course_name": "Computer Science Engineering",
            "course_code": "CSE",
            "org": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
        },
        "semester": {
            "id": "d4e5f6a7-b8c9-0123-def1-234567890123",
            "semester_name": "Fifth Semester",
            "sem_code": "SEM5"
        },
        "subject": {
            "id": "e5f6a7b8-c9d0-1234-ef12-345678901234",
            "subject_name": "Full Stack Development",
            "subject_code": "FSD"
        },
        "tech_skills": [
            {
                "id": "f6a7b8c9-d0e1-2345-f123-456789012345",
                "skill_name": "Django",
                "skill_code": "DJANGO"
            },
            {
                "id": "a7b8c9d0-e1f2-3456-1234-567890123456",
                "skill_name": "PostgreSQL",
                "skill_code": "PSQL"
            }
        ]
    }
]
```

**POST Request Body**:
```json
{
    "assignment_name": "React Frontend Development",
    "assignment_description": "Build a responsive frontend using React and Material-UI",
    "start_date": "2025-11-01T10:00:00Z",
    "submission_end_date": "2025-11-15T23:59:59Z",
    "total_marks": 100,
    "assignment_code": "FSD_A2",
    "course_id": "c3d4e5f6-a7b8-9012-cdef-123456789012",
    "semester_id": "d4e5f6a7-b8c9-0123-def1-234567890123",
    "subject_id": "e5f6a7b8-c9d0-1234-ef12-345678901234",
    "tech_skill_ids": [
        "a7b8c9d0-e1f2-3456-1234-567890123456",
        "b8c9d0e1-f2a3-4567-2345-678901234567"
    ]
}
```

**Validation Rules**:
- `assignment_code`: Must be unique
- `assignment_description`: Maximum 500 characters
- `start_date`: Must be in ISO 8601 format
- `submission_end_date`: Must be after start_date
- `total_marks`: Must be a positive integer
- `tech_skill_ids`: Must be a non-empty array of valid UUIDs

#### 10. Assignment Transactions (Submissions)

##### List/Create Assignment Submissions
**Endpoint**: `GET/POST /api/assignment-transactions/`

**GET Response** (With full nested data):
```json
[
    {
        "id": "d0e1f2a3-b4c5-6789-4567-890123456789",
        "obtained_marks": 85,
        "candidate_submit_date": "2025-10-28T14:30:00Z",
        "remarks": "Good implementation, well-structured code. Minor improvements needed in error handling.",
        "student": {
            "id": "a7b8c9d0-e1f2-3456-1234-567890123456",
            "student_usn_no": "1MS21CS001",
            "email": "student@example.com",
            "gender": "Male",
            "course": {
                "id": "c3d4e5f6-a7b8-9012-cdef-123456789012",
                "course_name": "Computer Science Engineering",
                "course_code": "CSE",
                "org": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
            }
        },
        "assignment": {
            "id": "c9d0e1f2-a3b4-5678-3456-789012345678",
            "assignment_name": "REST API Development",
            "assignment_description": "Create a RESTful API using Django REST Framework",
            "start_date": "2025-10-15T10:00:00Z",
            "submission_end_date": "2025-10-30T23:59:59Z",
            "total_marks": 100,
            "assignment_code": "FSD_A1",
            "course": { /* ... */ },
            "semester": { /* ... */ },
            "subject": { /* ... */ },
            "tech_skills": [ /* ... */ ]
        }
    }
]
```

**POST Request Body**:
```json
{
    "obtained_marks": 92,
    "remarks": "Excellent work! Code is clean and well-documented.",
    "student_id": "a7b8c9d0-e1f2-3456-1234-567890123456",
    "assignment_id": "c9d0e1f2-a3b4-5678-3456-789012345678"
}
```

**POST Response** (201 Created):
```json
{
    "id": "e1f2a3b4-c5d6-7890-5678-901234567890",
    "obtained_marks": 92,
    "candidate_submit_date": "2025-10-21T10:30:45Z",
    "remarks": "Excellent work! Code is clean and well-documented.",
    "student": { /* Full student object with nested course */ },
    "assignment": { /* Full assignment object with nested relationships */ }
}
```

**Validation Rules**:
- `obtained_marks`: Must be between 0 and the assignment's total_marks
- `remarks`: Required field
- `student_id`: Must be a valid UUID of an existing student
- `assignment_id`: Must be a valid UUID of an existing assignment
- `candidate_submit_date`: Auto-generated on creation (read-only)

---

## Authentication

### How JWT Authentication Works

1. **Login**: User sends credentials to `/api/token/`
2. **Receive Tokens**: Server returns `access` and `refresh` tokens
3. **Use Access Token**: Include in Authorization header for API requests
4. **Token Expiry**: Access token expires (default: 5 minutes)
5. **Refresh**: Use refresh token at `/api/token/refresh/` to get new access token

### Using Tokens in Requests

#### With cURL
```bash
curl -X GET http://127.0.0.1:8000/api/students/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

#### With Postman
1. Select Authorization tab
2. Choose "Bearer Token" type
3. Paste your access token

#### With JavaScript/Fetch
```javascript
fetch('http://127.0.0.1:8000/api/students/', {
    method: 'GET',
    headers: {
        'Authorization': 'Bearer ' + accessToken,
        'Content-Type': 'application/json'
    }
})
.then(response => response.json())
.then(data => console.log(data));
```

#### With Python Requests
```python
import requests

headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

response = requests.get('http://127.0.0.1:8000/api/students/', headers=headers)
data = response.json()
```

---

## Usage Examples

### Complete Workflow Example

#### Step 1: Login and Get Tokens
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

**Response**:
```json
{
    "access": "eyJ0eXAiOiJKV1Qi...",
    "refresh": "eyJ0eXAiOiJKV1Qi..."
}
```

#### Step 2: Create an Organization
```bash
curl -X POST http://127.0.0.1:8000/api/orgs/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1Qi..." \
  -H "Content-Type: application/json" \
  -d '{"name": "MIT College"}'
```

#### Step 3: Create a Course
```bash
curl -X POST http://127.0.0.1:8000/api/courses/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1Qi..." \
  -H "Content-Type: application/json" \
  -d '{
    "course_name": "Computer Science",
    "course_code": "CS",
    "org": "org-uuid-here"
  }'
```

#### Step 4: Create a Semester
```bash
curl -X POST http://127.0.0.1:8000/api/semesters/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1Qi..." \
  -H "Content-Type: application/json" \
  -d '{
    "semester_name": "Fifth Semester",
    "sem_code": "SEM5"
  }'
```

#### Step 5: Create a Subject
```bash
curl -X POST http://127.0.0.1:8000/api/subjects/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1Qi..." \
  -H "Content-Type: application/json" \
  -d '{
    "subject_name": "Full Stack Development",
    "subject_code": "FSD"
  }'
```

#### Step 6: Create Technical Skills
```bash
curl -X POST http://127.0.0.1:8000/api/tech-skills/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1Qi..." \
  -H "Content-Type: application/json" \
  -d '{"skill_name": "Django", "skill_code": "DJANGO"}'

curl -X POST http://127.0.0.1:8000/api/tech-skills/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1Qi..." \
  -H "Content-Type: application/json" \
  -d '{"skill_name": "React", "skill_code": "REACT"}'
```

#### Step 7: Register a Student
```bash
curl -X POST http://127.0.0.1:8000/api/students/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1Qi..." \
  -H "Content-Type: application/json" \
  -d '{
    "student_usn_no": "1MS21CS001",
    "email": "student@example.com",
    "gender": "Male",
    "course_id": "course-uuid-here"
  }'
```

#### Step 8: Create an Assignment
```bash
curl -X POST http://127.0.0.1:8000/api/assignments/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1Qi..." \
  -H "Content-Type: application/json" \
  -d '{
    "assignment_name": "Build REST API",
    "assignment_description": "Create a RESTful API using Django",
    "start_date": "2025-10-15T10:00:00Z",
    "submission_end_date": "2025-10-30T23:59:59Z",
    "total_marks": 100,
    "assignment_code": "FSD_A1",
    "course_id": "course-uuid-here",
    "semester_id": "semester-uuid-here",
    "subject_id": "subject-uuid-here",
    "tech_skill_ids": ["django-uuid", "postgres-uuid"]
  }'
```

#### Step 9: Submit an Assignment
```bash
curl -X POST http://127.0.0.1:8000/api/assignment-transactions/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1Qi..." \
  -H "Content-Type: application/json" \
  -d '{
    "obtained_marks": 85,
    "remarks": "Good implementation",
    "student_id": "student-uuid-here",
    "assignment_id": "assignment-uuid-here"
  }'
```

#### Step 10: Retrieve All Submissions
```bash
curl -X GET http://127.0.0.1:8000/api/assignment-transactions/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1Qi..."
```

---

## Project Structure

```
assignment-management-system/
├── backend/
│   ├── manage.py                     # Django management script
│   ├── api/                          # Main API application
│   │   ├── __init__.py
│   │   ├── admin.py                  # Django admin configuration
│   │   ├── apps.py                   # App configuration
│   │   ├── models.py                 # Database models
│   │   ├── serializers.py            # DRF serializers
│   │   ├── views.py                  # API views
│   │   ├── urls.py                   # API URL routing
│   │   ├── tests.py                  # Unit tests
│   │   └── migrations/               # Database migrations
│   │       ├── __init__.py
│   │       ├── 0001_initial.py       # Initial migration
│   │       └── __pycache__/
│   ├── core/                         # Project configuration
│   │   ├── __init__.py
│   │   ├── asgi.py                   # ASGI configuration
│   │   ├── settings.py               # Django settings
│   │   ├── urls.py                   # Main URL configuration
│   │   ├── wsgi.py                   # WSGI configuration
│   │   └── __pycache__/
│   └── env/                          # Virtual environment
│       ├── pyvenv.cfg
│       ├── Include/
│       ├── Lib/
│       │   └── site-packages/        # Installed packages
│       └── Scripts/                  # Virtual environment scripts
│           ├── activate              # Unix activation
│           ├── activate.bat          # Windows CMD activation
│           ├── Activate.ps1          # PowerShell activation
│           └── deactivate.bat
└── README.md                         # This file
```

### Key Files

#### `manage.py`
Django's command-line utility for administrative tasks.

**Common Commands**:
```powershell
python manage.py runserver          # Start development server
python manage.py makemigrations     # Create new migrations
python manage.py migrate            # Apply migrations
python manage.py createsuperuser    # Create admin user
python manage.py shell              # Open Django shell
python manage.py test               # Run tests
```

#### `api/models.py`
Contains all database models (User, Org, Course, Student, Assignment, etc.)

#### `api/serializers.py`
Converts complex data types to/from JSON for API responses.

#### `api/views.py`
Contains API view classes using Django REST Framework generics.

#### `api/urls.py`
Maps URL patterns to view classes for the API app.

#### `core/settings.py`
Main Django settings including database, installed apps, middleware, etc.

#### `core/urls.py`
Root URL configuration including admin and API routes.

---

## Development

### Running the Development Server
```powershell
cd backend
.\env\Scripts\Activate.ps1
python manage.py runserver
```

Access the API at: `http://127.0.0.1:8000/`

### Django Admin Interface
Access the admin panel at: `http://127.0.0.1:8000/admin/`

Use the superuser credentials created during setup.

### Making Database Changes

1. Modify models in `api/models.py`
2. Create migrations:
```powershell
python manage.py makemigrations
```

3. Review the migration file in `api/migrations/`
4. Apply migrations:
```powershell
python manage.py migrate
```

### Creating Test Data

Use Django shell:
```powershell
python manage.py shell
```

```python
from api.models import Org, Course, Semester

# Create an organization
org = Org.objects.create(name="Test University")

# Create a course
course = Course.objects.create(
    course_name="Computer Science",
    course_code="CS",
    org=org
)

# Create a semester
semester = Semester.objects.create(
    semester_name="Fifth Semester",
    sem_code="SEM5"
)
```

### Running Tests
```powershell
python manage.py test
```

For specific app:
```powershell
python manage.py test api
```

---

## Troubleshooting

### Common Issues and Solutions

#### 1. Database Connection Error
**Error**: `FATAL: password authentication failed for user "postgres"`

**Solution**:
- Verify PostgreSQL is running
- Check credentials in `settings.py`
- Ensure database `fsd_assignment` exists
- Test connection using pgAdmin or psql

#### 2. Migration Errors
**Error**: `No migrations to apply` or `Relation does not exist`

**Solution**:
```powershell
python manage.py makemigrations api
python manage.py migrate
```

If issues persist:
```powershell
# Delete migration files (except __init__.py)
# Delete database tables
python manage.py makemigrations
python manage.py migrate
```

#### 3. JWT Token Invalid
**Error**: `{"detail": "Given token not valid for any token type"}`

**Solution**:
- Token may be expired - request a new token using `/api/token/`
- Ensure token is correctly formatted: `Bearer <token>`
- Check token hasn't been manually modified

#### 4. Virtual Environment Not Activating
**Error**: Execution policy restriction in PowerShell

**Solution**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### 5. Import Errors
**Error**: `ModuleNotFoundError: No module named 'rest_framework'`

**Solution**:
```powershell
# Ensure virtual environment is activated
.\env\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```

#### 6. Port Already in Use
**Error**: `Error: That port is already in use.`

**Solution**:
```powershell
# Use a different port
python manage.py runserver 8001

# Or find and kill the process using port 8000
netstat -ano | findstr :8000
taskkill /PID <process_id> /F
```

#### 7. CORS Issues (If accessing from frontend)
**Error**: Cross-Origin Request Blocked

**Solution**:
Install django-cors-headers:
```powershell
pip install django-cors-headers
```

Update `settings.py`:
```python
INSTALLED_APPS = [
    # ...
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    # ...
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

---

## API Response Status Codes

### Success Codes
- **200 OK**: Request successful (GET, PUT, PATCH)
- **201 Created**: Resource created successfully (POST)
- **204 No Content**: Request successful, no content to return (DELETE)

### Client Error Codes
- **400 Bad Request**: Invalid request data
- **401 Unauthorized**: Missing or invalid authentication token
- **403 Forbidden**: Authenticated but not authorized
- **404 Not Found**: Resource doesn't exist
- **409 Conflict**: Duplicate unique field (e.g., student_usn_no)

### Server Error Codes
- **500 Internal Server Error**: Unexpected server error

---

## API Error Responses

### Validation Error Example
```json
{
    "student_usn_no": ["This field is required."],
    "email": ["Enter a valid email address."]
}
```

### Authentication Error Example
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### Not Found Error Example
```json
{
    "detail": "Not found."
}
```

---

## Best Practices

### API Usage
1. Always include the JWT token in the Authorization header
2. Use UUIDs when referencing related objects
3. Handle token expiration by refreshing tokens
4. Validate data before sending POST requests
5. Use proper HTTP methods (GET for retrieval, POST for creation)

### Database
1. Always use transactions for related operations
2. Create database backups regularly
3. Use migrations for schema changes
4. Index frequently queried fields

### Security
1. Never commit `SECRET_KEY` to version control
2. Use environment variables for sensitive data
3. Set `DEBUG = False` in production
4. Keep dependencies updated
5. Use HTTPS in production

---

## Future Enhancements

Potential features to add:
- User registration endpoint
- Password reset functionality
- File upload for assignment submissions
- Email notifications for assignment deadlines
- Assignment grading workflow
- Professor-specific permissions
- Student dashboard API
- Search and filter capabilities
- Pagination for large datasets
- Bulk operations (create multiple students)
- Assignment templates
- Export data to CSV/PDF
- Analytics and reporting endpoints

---

## Contributors

Created by: [Your Name]
Institution: [Your College/University]
Course: Full Stack Development
Date: October 2025

---

## Academic Context

This Assignment Management System was developed as part of the Full Stack Development (FSD) course curriculum. It demonstrates practical implementation of:

- Backend API development with Django
- Database design and normalization
- RESTful API principles
- JWT authentication and authorization
- ORM (Object-Relational Mapping) with Django
- PostgreSQL database management
- Serialization and deserialization
- API documentation and best practices
