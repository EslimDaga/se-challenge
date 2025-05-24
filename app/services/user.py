"""User service layer for business logic."""

from typing import Optional, List, Tuple
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from loguru import logger

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    """Service class for user operations."""

    @staticmethod
    async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
        """Create a new user."""
        try:
            now = datetime.now(timezone.utc)
            db_user = User(**user_data.model_dump(), created_at=now, updated_at=now)
            db.add(db_user)
            await db.commit()
            await db.refresh(db_user)
            logger.info(f"User created successfully: {db_user.username}")
            return db_user
        except IntegrityError as e:
            await db.rollback()
            logger.error(f"Failed to create user: {str(e)}")
            if "username" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already exists",
                ) from e
            elif "email" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists",
                ) from e
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User creation failed",
                ) from e

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
        """Get user by ID."""
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user:
            if user.created_at is None or user.updated_at is None:
                await UserService._fix_user_timestamps(db, user)
            logger.info(f"User retrieved: {user.username}")
        else:
            logger.warning(f"User not found with ID: {user_id}")
        return user

    @staticmethod
    async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
        """Get user by username."""
        result = await db.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()
        if user and (user.created_at is None or user.updated_at is None):
            await UserService._fix_user_timestamps(db, user)
        return user

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
        """Get user by email."""
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if user and (user.created_at is None or user.updated_at is None):
            await UserService._fix_user_timestamps(db, user)
        return user

    @staticmethod
    async def get_users(
        db: AsyncSession, skip: int = 0, limit: int = 100, active_only: bool = True
    ) -> Tuple[List[User], int]:
        """Get users with pagination."""
        await UserService._fix_all_user_timestamps(db)

        query = select(User)

        if active_only:
            query = query.where(User.active)

        query = query.order_by(User.created_at.desc())
        result = await db.execute(query)
        all_users = result.scalars().all()

        total = len(all_users)
        users = list(all_users)[skip : skip + limit]

        logger.info(f"Retrieved {len(users)} users (total: {total})")
        return users, total

    @staticmethod
    async def _fix_user_timestamps(db: AsyncSession, user: User) -> None:
        """Fix None timestamps for a single user."""
        now = datetime.now(timezone.utc)
        if user.created_at is None:
            user.created_at = now
        if user.updated_at is None:
            user.updated_at = now
        await db.commit()
        await db.refresh(user)

    @staticmethod
    async def _fix_all_user_timestamps(db: AsyncSession) -> None:
        """Fix None timestamps for all users."""
        now = datetime.now(timezone.utc)

        await db.execute(
            update(User).where(User.created_at.is_(None)).values(created_at=now)
        )

        await db.execute(
            update(User).where(User.updated_at.is_(None)).values(updated_at=now)
        )

        await db.commit()

    @staticmethod
    async def update_user(
        db: AsyncSession, user_id: int, user_data: UserUpdate
    ) -> Optional[User]:
        """Update user."""
        db_user = await UserService.get_user_by_id(db, user_id)
        if not db_user:
            return None

        try:
            update_data = user_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_user, field, value)

            db_user.updated_at = datetime.now(timezone.utc)

            await db.commit()
            await db.refresh(db_user)
            logger.info(f"User updated successfully: {db_user.username}")
            return db_user
        except IntegrityError as e:
            await db.rollback()
            logger.error(f"Failed to update user: {str(e)}")
            if "username" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already exists",
                ) from e
            elif "email" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists",
                ) from e
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="User update failed"
                ) from e

    @staticmethod
    async def delete_user(db: AsyncSession, user_id: int) -> bool:
        """Delete user (soft delete by setting active=False)."""
        db_user = await UserService.get_user_by_id(db, user_id)
        if not db_user:
            return False

        db_user.active = False
        db_user.updated_at = datetime.now(timezone.utc)
        await db.commit()
        logger.info(f"User deleted (soft): {db_user.username}")
        return True

    @staticmethod
    async def hard_delete_user(db: AsyncSession, user_id: int) -> bool:
        """Hard delete user from database."""
        db_user = await UserService.get_user_by_id(db, user_id)
        if not db_user:
            return False

        await db.delete(db_user)
        await db.commit()
        logger.info(f"User hard deleted: {db_user.username}")
        return True
