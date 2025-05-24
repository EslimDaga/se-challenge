"""Schemas for user management."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from app.models.user import UserRoleEnum


class UserBase(BaseModel):
    """Base user schema with common fields."""

    username: str = Field(
        ..., min_length=3, max_length=50, description="Unique username"
    )
    email: EmailStr = Field(..., description="User email address")
    first_name: str = Field(
        ..., min_length=1, max_length=100, description="User first name"
    )
    last_name: str = Field(
        ..., min_length=1, max_length=100, description="User last name"
    )
    role: UserRoleEnum = Field(default=UserRoleEnum.USER, description="User role")
    active: bool = Field(default=True, description="User active status")


class UserCreate(UserBase):
    """Schema for creating a new user."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "johndoe",
                "email": "john@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "role": "user",
                "active": True,
            }
        }
    )


class UserUpdate(BaseModel):
    """Schema for updating an existing user."""

    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    role: Optional[UserRoleEnum] = None
    active: Optional[bool] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "first_name": "Jane",
                "last_name": "Smith",
                "email": "jane@example.com",
            }
        }
    )


class UserResponse(UserBase):
    """Schema for user response."""

    id: int = Field(..., description="User ID")
    created_at: Optional[datetime] = Field(None, description="User creation timestamp")
    updated_at: Optional[datetime] = Field(
        None, description="User last update timestamp"
    )

    model_config = ConfigDict(from_attributes=True)


class UserListResponse(BaseModel):
    """Schema for paginated user list response."""

    users: List[UserResponse]
    total: int = Field(..., description="Total number of users")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Page size")
    pages: int = Field(..., description="Total number of pages")


class ErrorResponse(BaseModel):
    """Schema for error responses."""

    detail: str = Field(..., description="Error message")
