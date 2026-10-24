from database.connection import get_db 
from fastapi import Depends 
from repositories.implementations.sqlalchemy_auth_repository import AuthRepository 
from services.auth_service import AuthService 
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.interfaces.auth_repository import AuthRepositoryInterface

def get_auth_repository(db:AsyncSession = Depends(get_db))  : 
    return AuthRepository(db) 

def get_auth_service(
    db:AsyncSession = Depends(get_db) , 
    repository:AuthRepositoryInterface = Depends(get_auth_repository)
    ):
    return AuthService(db , repository)