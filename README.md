# Blog CMS API - FastAPI Project

A professional Blog/CMS RESTful API built with FastAPI, MySQL, and SQLAlchemy (Async).

## Features

- ✅ Full async/await support
- ✅ SQLAlchemy 2.0 with async MySQL
- ✅ Pydantic v2 for validation
- ✅ CRUD operations for Users, Posts, Categories, Comments
- ✅ Database migrations with Alembic
- ✅ Industrial project structure
- ✅ API versioning
- 🔜 JWT Authentication (Next phase)
- 🔜 OAuth2 (Next phase)
- 🔜 RBAC - Role-Based Access Control (Next phase)

## Project Structure

```
blog-cms-api/
├── app/
│   ├── api/v1/endpoints/     # API endpoints
│   ├── crud/                 # Database operations
│   ├── db/                   # Database configuration
│   ├── models/               # SQLAlchemy models
│   ├── schemas/              # Pydantic schemas
│   ├── utils/                # Utilities
│   └── main.py               # FastAPI application
├── alembic/                  # Database migrations
└── tests/                    # Unit tests
```

## Setup Instructions

### 1. Prerequisites

- Python 3.11+
- MySQL 8.0+
- pip

### 2. Installation

```bash
# Clone repository
git clone <your-repo>
cd blog-cms-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Database Setup

```bash
# Create MySQL database
mysql -u root -p
CREATE DATABASE blog_cms;
EXIT;
```

### 4. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your database credentials
DATABASE_URL=mysql+aiomysql://root:your_password@localhost:3306/blog_cms
DATABASE_URL_SYNC=mysql+pymysql://root:your_password@localhost:3306/blog_cms
```

### 5. Database Migration

```bash
# Initialize Alembic (first time only)
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Run migrations
alembic upgrade head
```

### 6. Run Application

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Users
- `POST /api/v1/users/` - Create user
- `GET /api/v1/users/` - List users
- `GET /api/v1/users/{id}` - Get user
- `PUT /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Delete user

### Categories
- `POST /api/v1/categories/` - Create category
- `GET /api/v1/categories/` - List categories
- `GET /api/v1/categories/{id}` - Get category
- `PUT /api/v1/categories/{id}` - Update category
- `DELETE /api/v1/categories/{id}` - Delete category

### Posts
- `POST /api/v1/posts/` - Create post
- `GET /api/v1/posts/` - List posts
- `GET /api/v1/posts/{id}` - Get post
- `GET /api/v1/posts/slug/{slug}` - Get post by slug
- `PUT /api/v1/posts/{id}` - Update post
- `DELETE /api/v1/posts/{id}` - Delete post

### Comments
- `POST /api/v1/comments/` - Create comment
- `GET /api/v1/comments/` - List comments
- `GET /api/v1/comments/post/{post_id}` - Get comments by post
- `GET /api/v1/comments/{id}` - Get comment
- `PUT /api/v1/comments/{id}` - Update comment
- `DELETE /api/v1/comments/{id}` - Delete comment

## Example Usage

### Create a User
```bash
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "full_name": "John Doe",
    "password": "strongpassword123"
  }'
```

### Create a Category
```bash
curl -X POST "http://localhost:8000/api/v1/categories/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Technology",
    "slug": "technology",
    "description": "Tech articles and tutorials"
  }'
```

### Create a Post
```bash
curl -X POST "http://localhost:8000/api/v1/posts/?author_id=1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Getting Started with FastAPI",
    "slug": "getting-started-fastapi",
    "content": "FastAPI is a modern web framework...",
    "excerpt": "Learn FastAPI basics",
    "is_published": true,
    "category_id": 1
  }'
```

## Next Steps - Security Implementation

When you're ready, we'll implement:

1. **Password Hashing** (bcrypt)
2. **JWT Authentication**
3. **OAuth2 with Bearer tokens**
4. **RBAC (Role-Based Access Control)**
   - Admin: Full access
   - Editor: Manage posts/categories
   - Author: Manage own posts
   - User: Read and comment

## Development

```bash
# Run tests
pytest

# Check code style
black app/
flake8 app/

# Type checking
mypy app/
```
