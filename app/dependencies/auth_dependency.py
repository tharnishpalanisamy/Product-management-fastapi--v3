from app.database.connection import get_db 
from fastapi import Depends 
from app.repositories.implementations.sqlalchemy_user_repository import UserRepository 
from app.services.auth_service import AuthService 
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.interfaces.user_repository import UserRepositoryInterface

def get_auth_repository(db:AsyncSession = Depends(get_db))  : 
    return UserRepository(db) 

def get_auth_service(
    db:AsyncSession = Depends(get_db) , 
    repository:UserRepositoryInterface = Depends(get_auth_repository)
    ):
    return AuthService(db , repository)


def current_user() : 
    pass    