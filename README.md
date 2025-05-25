# 🚀 User Management API

A robust and scalable user management API built with FastAPI, SQLAlchemy, and MySQL. This project provides a complete CRUD (Create, Read, Update, Delete) interface for user management with features like pagination, filtering, soft deletes, and comprehensive testing.

## 🖼️ Frontend Preview

![User Management API Preview](https://raw.githubusercontent.com/EslimDaga/se-challenge/refs/heads/main/preview.jpeg)

### 🔗 Related Repositories

- **Frontend Application**: [se-challenge-frontend](https://github.com/EslimDaga/se-challenge-frontend)
- **Live Demo**: [https://se-challenge-frontend.vercel.app/](https://se-challenge-frontend.vercel.app/)

---

## ⚡ Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/EslimDaga/se-challenge
cd se-challenge
```

### 2. Create Virtual Environment

```bash
python -m venv env | python3 -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Setup

Create a `.env` file in the root directory:

```env
DATABASE_URL=mysql+aiomysql://username:password@host:port/database
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=database
```

### 5. Database Setup

🔹 **Before proceeding, make sure you have created the database in your MySQL server.**
You can create it with the following command (adjust the name and settings as needed):

```sql
CREATE DATABASE se_challenge CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Run Alembic migrations to create the database schema:

```bash
alembic upgrade head
```

### 6. Run the Application

```bash
# Development mode
python app/main.py

# Or using uvicorn directly
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at:
- **API Base URL**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc

## 📚 API Documentation

### Health Check Endpoints

- `GET /` - Root health check
- `GET /health` - Detailed health status

### User Management Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/users/` | Create a new user |
| `GET` | `/api/v1/users/` | Get all users (paginated) |
| `GET` | `/api/v1/users/{user_id}` | Get user by ID |
| `PUT` | `/api/v1/users/{user_id}` | Update user |
| `DELETE` | `/api/v1/users/{user_id}` | Soft delete user |
| `DELETE` | `/api/v1/users/{user_id}/hard` | Hard delete user |

### Example Usage

#### Create a User

```bash
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "user",
    "active": true
  }'
```

#### Get Users with Pagination

```bash
curl "http://localhost:8000/api/v1/users/?page=1&size=10&active_only=true"
```

#### Update a User

```bash
curl -X PUT "http://localhost:8000/api/v1/users/1" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jane",
    "email": "jane@example.com"
  }'
```

## 🧪 Testing

The project includes comprehensive test coverage for all endpoints and business logic.

### Run All Tests

```bash
pytest
```

### Run Specific Test Categories

```bash
# Unit tests only
pytest -m unit

# Database tests
pytest -m database

# Integration tests
pytest app/tests/test_user_api.py
```

### Run Tests with Coverage

```bash
pytest --cov=app --cov-report=html
```

## 🏗️ Project Structure

```
se-challenge/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── api/
│   │   └── v1/
│   │       ├── api.py          # API router aggregation
│   │       └── routes/
│   │           └── user.py     # User endpoints
│   ├── core/
│   │   ├── config.py           # Application settings
│   │   └── logging.py          # Logging configuration
│   ├── db/
│   │   ├── base.py             # SQLAlchemy base model
│   │   └── session.py          # Database session management
│   ├── models/
│   │   └── user.py             # User SQLAlchemy model
│   ├── schemas/
│   │   └── user.py             # Pydantic schemas
│   ├── services/
│   │   └── user.py             # Business logic layer
│   └── tests/
│       ├── conftest.py         # Test configuration
│       ├── test_user_api.py    # API integration tests
│       └── unit/
│           └── test_database_connection.py
├── alembic/                    # Database migrations
├── requirements.txt
├── alembic.ini
├── pytest.ini
├── .env
└── README.md
```

## 🔧 Configuration

The application uses environment variables for configuration. Key settings include:

- **Database Configuration**: Connection strings and credentials
- **API Settings**: Version, CORS origins, project metadata
- **Logging**: Log level configuration
- **Server**: Host, port, and reload settings

All settings are managed through the `app/core/config.py` file using Pydantic Settings.

## 🗄️ Database Schema

### Users Table

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary key (auto-increment) |
| `username` | VARCHAR(50) | Unique username |
| `email` | VARCHAR(255) | Unique email address |
| `first_name` | VARCHAR(100) | User's first name |
| `last_name` | VARCHAR(100) | User's last name |
| `role` | ENUM | User role (admin, user, guest) |
| `active` | BOOLEAN | User active status |
| `created_at` | DATETIME | Creation timestamp |
| `updated_at` | DATETIME | Last update timestamp |

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support, please open an issue in the GitHub repository or contact the development team.

## 🔄 Changelog

### v1.0.0
- Initial release
- Complete CRUD operations for users
- Pagination and filtering
- Comprehensive test coverage
- API documentation
- Database migrations setup

---

**Built with ❤️ using FastAPI**