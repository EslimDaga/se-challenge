"""Database session management for SQLAlchemy."""

from enum import Enum as PyEnum
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, Enum, Integer
from app.db.base import Base


class UserRole(PyEnum):
    """User roles enumeration"""

    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class User(Base):
    """User model"""

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        unique=True,
        autoincrement=True,
    )

    username = Column(String(50), nullable=False, index=True, unique=True)

    email = Column(
        String(255),
        nullable=False,
        unique=True,
    )

    first_name = Column(
        String(100),
        nullable=False,
    )

    last_name = Column(
        String(100),
        nullable=False,
    )

    role = Column(
        Enum(UserRole, name="user_role"),
        nullable=False,
        default=UserRole.USER,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    active = Column(
        Boolean,
        default=True,
        nullable=False,
    )
