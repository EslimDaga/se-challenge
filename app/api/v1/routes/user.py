"""Routes for user management."""

import math
from fastapi import APIRouter, HTTPException, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from app.db.session import get_db
from app.services.user import UserService
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserListResponse,
    ErrorResponse,
)

router = APIRouter(
    tags=["users"],
    responses={
        404: {"model": ErrorResponse, "description": "Not found"},
        400: {"model": ErrorResponse, "description": "Bad request"},
        422: {"model": ErrorResponse, "description": "Validation error"},
    },
)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Create a new user with the provided information.",
    responses={
        201: {"description": "User created successfully"},
        400: {"description": "Username or email already exists"},
        422: {"description": "Validation error"},
    },
)
async def create_user(
    user: UserCreate, db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """
    Create a new user.

    **Example request:**
    ```json
    {
        "username": "johndoe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "role": "user",
        "active": true
    }
    ```
    """
    logger.info(f"Creating user: {user.username}")

    existing_user = await UserService.get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )

    existing_email = await UserService.get_user_by_email(db, user.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
        )

    db_user = await UserService.create_user(db, user)
    return UserResponse.model_validate(db_user)


@router.get(
    "/",
    response_model=UserListResponse,
    summary="Get all users",
    description="Retrieve a paginated list of users.",
    responses={
        200: {"description": "Users retrieved successfully"},
    },
)
async def get_users(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size"),
    active_only: bool = Query(True, description="Filter active users only"),
    db: AsyncSession = Depends(get_db),
) -> UserListResponse:
    """
    Get all users with pagination.

    **Example response:**
    ```json
    {
        "users": [...],
        "total": 50,
        "page": 1,
        "size": 10,
        "pages": 5
    }
    ```
    """
    logger.info(f"Getting users: page={page}, size={size}, active_only={active_only}")

    skip = (page - 1) * size
    users, total = await UserService.get_users(
        db, skip=skip, limit=size, active_only=active_only
    )

    pages = math.ceil(total / size) if total > 0 else 1

    return UserListResponse(
        users=[UserResponse.model_validate(user) for user in users],
        total=total,
        page=page,
        size=size,
        pages=pages,
    )


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
    description="Retrieve a specific user by their ID.",
    responses={
        200: {"description": "User retrieved successfully"},
        404: {"description": "User not found"},
        400: {"description": "Invalid user ID"},
    },
)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)) -> UserResponse:
    """
    Get a user by ID.

    **Example response:**
    ```json
    {
        "id": 1,
        "username": "johndoe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "role": "user",
        "active": true,
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    }
    ```
    """
    logger.info(f"Getting user: {user_id}")

    if user_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID"
        )

    db_user = await UserService.get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return UserResponse.model_validate(db_user)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update user",
    description="Update a user's information.",
    responses={
        200: {"description": "User updated successfully"},
        404: {"description": "User not found"},
        400: {"description": "Invalid user ID or username/email already exists"},
        422: {"description": "Validation error"},
    },
)
async def update_user(
    user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """
    Update a user by ID.

    **Example request:**
    ```json
    {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane@example.com"
    }
    ```
    """
    logger.info(f"Updating user: {user_id}")

    if user_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID"
        )

    existing_user = await UserService.get_user_by_id(db, user_id)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if user.username and user.username != existing_user.username:
        username_user = await UserService.get_user_by_username(db, user.username)
        if username_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists",
            )

    if user.email and user.email != existing_user.email:
        email_user = await UserService.get_user_by_email(db, user.email)
        if email_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
            )

    updated_user = await UserService.update_user(db, user_id, user)
    return UserResponse.model_validate(updated_user)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user",
    description="Soft delete a user (set active=False).",
    responses={
        204: {"description": "User deleted successfully"},
        404: {"description": "User not found"},
        400: {"description": "Invalid user ID"},
    },
)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)) -> None:
    """
    Delete a user by ID (soft delete).

    This endpoint performs a soft delete by setting the user's active status to False.
    """
    logger.info(f"Deleting user: {user_id}")

    if user_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID"
        )

    deleted = await UserService.delete_user(db, user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@router.delete(
    "/{user_id}/hard",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Hard delete user",
    description="Permanently delete a user from the database.",
    responses={
        204: {"description": "User permanently deleted"},
        404: {"description": "User not found"},
        400: {"description": "Invalid user ID"},
    },
)
async def hard_delete_user(user_id: int, db: AsyncSession = Depends(get_db)) -> None:
    """
    Hard delete a user by ID.
    """
    logger.info(f"Hard deleting user: {user_id}")

    if user_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID"
        )

    deleted = await UserService.hard_delete_user(db, user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
