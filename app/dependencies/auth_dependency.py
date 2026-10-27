from app.database.connection import get_db 
from fastapi import Depends , HTTPException , status
from app.repositories.implementations.sqlalchemy_user_repository import UserRepository 
from app.services.auth_service import AuthService 
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.interfaces.user_repository import UserRepositoryInterface
from fastapi.security import HTTPBearer , HTTPAuthorizationCredentials
from jwt.exceptions import InvalidTokenError  
from app.config import setting
import jwt 
from sqlalchemy import select 
from app.models import User


def get_auth_repository(db:AsyncSession = Depends(get_db))  : 
    return UserRepository(db) 

def get_auth_service(
    db:AsyncSession = Depends(get_db) , 
    repository:UserRepositoryInterface = Depends(get_auth_repository)
    ):
    return AuthService(db , repository)

bearer_scheme = HTTPBearer(auto_error=False)    

async def get_current_user(
    credentials:HTTPAuthorizationCredentials = Depends(bearer_scheme), 
    db:AsyncSession = Depends(get_db)
) : 

    token = credentials.credentials 

    try :
        payload = jwt.decode(
            token , 
            setting.JWT_SECRET_KEY , 
            algorithms=[setting.JWT_ALGORITHM] 
        )

        user_id = int(payload.get('sub'))

        if user_id is None :
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

    statement = select(User).where(
        User.id == user_id
    )

    user = await db.scalar(statement) 
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user



def admin_required( current_user:User = Depends(get_current_user) ) -> User :
    if current_user.role != 'admin' :
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user