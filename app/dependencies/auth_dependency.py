from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.email_client import EmailClient
from app.config import setting
from app.database.connection import get_db
from app.models import User
from app.repositories.implementations.sqlalchemy_refresh_token_repository import (
    RefreshTokenRepository,
)
from app.repositories.implementations.sqlalchemy_user_repository import UserRepository
from app.repositories.interfaces.refresh_token_repository import (
    RefreshTokenRepositoryInterface,
)
from app.repositories.interfaces.user_repository import UserRepositoryInterface
from app.services.auth_service import AuthService
from app.services.email_service import EmailService
from app.services.refresh_token_service import RefreshTokenService


def get_auth_repository(db: AsyncSession = Depends(get_db)):
    return UserRepository(db)


def get_refresh_token_repository(db: AsyncSession = Depends(get_db)):
    return RefreshTokenRepository(db)


def get_refresh_token_service(
    db: AsyncSession = Depends(get_db),
    repository: RefreshTokenRepositoryInterface = Depends(get_refresh_token_repository),
):

    return RefreshTokenService(db, repository)


def get_email_client():
    return EmailClient()


def get_email_service(
    email_client: Annotated[EmailClient, Depends(get_email_client)],
):
    return EmailService(email_client)


def get_auth_service(
    db: AsyncSession = Depends(get_db),
    repository: UserRepositoryInterface = Depends(get_auth_repository),
    refresh_token_service: RefreshTokenService = Depends(get_refresh_token_service),
    email_service=Depends(get_email_service),
):
    return AuthService(db, repository, refresh_token_service , email_service)


bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
):

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token, setting.JWT_SECRET_KEY, algorithms=[setting.JWT_ALGORITHM]
        )

        user_id = int(payload.get("sub"))

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    statement = select(User).where(User.id == user_id)

    user = await db.scalar(statement)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


def admin_required(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user
