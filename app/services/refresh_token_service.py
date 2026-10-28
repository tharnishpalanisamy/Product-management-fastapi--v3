import hashlib 
import secrets
from datetime import datetime , timezone , timedelta 
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import RefreshToken
from app.repositories.implementations import RefreshTokenRepository 

class RefreshTokenService:
    REFRESH_TOKEN_EXPIRE_DAYS = 7

    def __init__(self , db , repository ) : 
        self.db = db 
        self.repository = repository 

    @staticmethod
    def generate_token() -> str:
        return secrets.token_urlsafe(64)

    @staticmethod
    def hash_token(token: str) -> str:
        return hashlib.sha256(
            token.encode("utf-8")
        ).hexdigest()

    async def issue_refresh_token(
        self , 
        user_id : int 
        ) : 

        token = self.generate_token() 

        hashed_token = self.hash_token(token) 

        expires_at = datetime.noe(timezone.utc) + timedelta(
            days=self.REFRESH_TOKEN_EXPIRE_DAYS
        )  

        refresh_token = RefreshToken(
            user_id = user_id , 
            token_hash = hashed_token ,
            expires_at = expires_at  
        )

        try :
            await self.repository.create(refresh_token) 
            await self.db.commit() 

        except Exception :
            self.db.rollback() 
            raise

        return token  
    
    