import hashlib 
import secrets
from datetime import datetime , timezone , timedelta 
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import RefreshToken
from app.repositories.implementations import RefreshTokenRepository 
from app.exceptions import InvalidRefreshTokenException

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
    

    def _build_refresh_token_record(
        self,
        user_id: int,
    ) :
        raw_token = self.generate_token() 

        token_record = RefreshToken(
            user_id=user_id,
            token_hash=self.hash_token(raw_token),
            expires_at=(
                datetime.now(timezone.utc)
                + timedelta(days=self.REFRESH_TOKEN_EXPIRE_DAYS)
            ),
        )

        return raw_token, token_record


    async def issue_refresh_token(
        self , 
        user_id : int 
        ) : 

        token = self.generate_token() 

        hashed_token = self.hash_token(token) 

        expires_at = datetime.now(timezone.utc) + timedelta(
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
            await self.db.rollback() 
            raise

        return token  

    async def rotate_refresh_token(
        self , raw_token : str 
    ) : 
        token_hash = self.hash_token(raw_token) 

        try :
            old_record = await self.repository.get_by_hash_for_update(
                token_hash
            )

            if old_record is None :
                raise InvalidRefreshTokenException() 

            now = datetime.now(timezone.utc) 

            if old_record.revoked_at is not None :
                await self.repository.revoke_all_active_for_user(
                    old_record.user_id,
                    now,
                )
                await self.db.commit() 
                raise InvalidRefreshTokenException()  

            expires_at = old_record.expires_at

            if expires_at.tzinfo is None:
                expires_at = expires_at.replace(tzinfo=timezone.utc)

            if expires_at <= now:
                old_record.revoked_at = now
                await self.db.commit()
                raise InvalidRefreshTokenException()

            user_id = old_record.user_id

            # Create replacement without committing independently.
            new_raw_token, new_record = (
                self._build_refresh_token_record(user_id)
            )

            self.db.add(new_record)
            await self.db.flush()

            old_record.revoked_at = now
            old_record.replaced_by_id = new_record.id

            await self.db.flush()
            await self.db.commit()

            return user_id, new_raw_token

        except InvalidRefreshTokenException:
            raise
        except Exception:
            await self.db.rollback()
            raise


            
    

        
    