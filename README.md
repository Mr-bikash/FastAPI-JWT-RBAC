# FastAPI JWT Authentication with Role-Based Access Control (RBAC)

## Overview

A secure RESTful API with JWT authentication and Role-Based Access Control (RBAC) using FastAPI and PostgreSQL. The API allows user registration, authentication, and role-based access to protected resources.

## Features

- ✅ User registration and authentication
- 🔐 JWT token-based authentication
- 👥 Role-Based Access Control (Admin and User roles)
- 🛡️ Secure password hashing with bcrypt
- 🗃️ PostgreSQL database integration
- 🏗️ CRUD operations for projects with role-based permissions
- 📝 Interactive API documentation (Swagger UI and ReDoc)

## Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)

## Installation

1. **Clone the repository**
    ```bash
    git clone https://github.com/Mr-bikash/FastAPI-JWT-RBAC.git
    cd fastapi-jwt-rbac

2. **Create and Activate Virtual Environment**
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install Dependencies**
    pip install -r requirements.txt

4. **Set up PostgreSQL**
    Create a new database
    Note your database credentials

5. **Configure environment variables**
    Create .env file:
        DATABASE_URL=postgresql://username:password@localhost:5432/database-name
        SECRET_KEY=your-strong-secret-key-here
        ALGORITHM=HS256
        ACCESS_TOKEN_EXPIRE_MINUTES=30

### GENERATE SECRET KEY USING THE FOLLOWING COMMANDS
    import secrets
    print(secrets.token_urlsafe(32))

### Section 4: Running and Documentation
```markdown
## Running the Application

Start the server:
```bash
uvicorn app.main:app --reload

Access API documentation:
    Swagger UI: http://localhost:8000/docs
    ReDoc: http://localhost:8000/redoc


### Section 5: API Endpoints
```markdown
## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | `/register` | Register new user |
| POST   | `/login` | Login to get JWT |

### Projects (Require JWT)

| Method | Endpoint | Role Required |
|--------|----------|---------------|
| GET    | `/projects` | User/Admin |
| POST   | `/projects` | Admin only |
| GET    | `/projects/{id}` | User/Admin |
| PUT    | `/projects/{id}` | Admin only |
| DELETE | `/projects/{id}` | Admin only |

## Usage Examples

### Register User
```bash
curl -X POST "http://localhost:8000/register" \
-H "Content-Type: application/json" \
-d '{"username": "admin1", "password": "mypassword", "role": "admin"}'

### Login
curl -X POST "http://localhost:8000/login" \
-H "Content-Type: application/json" \
-d '{"username": "admin1", "password": "mypassword"}'

### Create Project (Admin)
curl -X POST "http://localhost:8000/projects" \
-H "Authorization: Bearer YOUR_JWT_TOKEN" \
-H "Content-Type: application/json" \
-d '{"name": "My Project", "description": "Project description"}'


### Section 7: Database and Security
```markdown
## Database Schema

**users** table:
- id (PK)
- username (Unique)
- hashed_password
- role ('admin' or 'user')

**projects** table:
- id (PK)
- name
- description
- owner_id (FK to users.id)

## Security Best Practices

1. Always use HTTPS in production
2. Keep secret keys out of version control
3. Implement proper password policies
4. Regularly rotate JWT secret keys
5. Use environment variables for configuration

## Deployment

For production:
1. Use Gunicorn with Uvicorn workers
2. Configure PostgreSQL connection pooling
3. Set up Nginx reverse proxy
4. Implement proper monitoring
