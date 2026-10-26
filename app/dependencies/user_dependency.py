from app.database.connection import get_db 
from fastapi import Depends , HTTPException , status
from app.repositories.implementations.sqlalchemy_user_repository import UserRepository 
from app.services.user_service import UserService 
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.interfaces.user_repository import UserRepositoryInterface



def get_user_repository(db:AsyncSession = Depends(get_db))  : 
    return UserRepository(db) 

def get_user_service(
    db:AsyncSession = Depends(get_db) , 
    repository:UserRepositoryInterface = Depends(get_user_repository)
    ):
    return UserService(db , repository)


