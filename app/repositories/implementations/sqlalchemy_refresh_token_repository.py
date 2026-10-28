
from sqlalchemy import select , update
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from app.models import RefreshToken


class RefreshTokenRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        data: RefreshToken,
    ) -> RefreshToken:
        
        self.db.add(data)
        await self.db.flush()
        return data

    async def get_by_hash(
        self,
        token_hash: str,
    ) -> RefreshToken | None:
        
        query = select(RefreshToken).where(
            RefreshToken.token_hash == token_hash
        )

        return await self.db.scalar(query)

    async def revoke(
        self,
        refresh_token: RefreshToken,
        revoked_at,
    ) -> RefreshToken:
        
        refresh_token.revoked_at = revoked_at
        await self.db.flush()
        return refresh_token


    async def get_by_hash_for_update(
        self , 
        hash 
        ) : 

        query = select(RefreshToken).where(
            RefreshToken.token_hash == hash 
        ).with_for_update().execution_options(populate_existing=True)

        result = await self.db.scalar(query)
        return result 

    async def revoke_all_active_for_user(
        self , 
        user_id:int , 
        revoked_at : datetime 
    ):
        query = update(RefreshToken).where(
            RefreshToken.user_id == user_id , 
            RefreshToken.revoked_at.is_(None)
        ).values(revoked_at = revoked_at) 

        await self.db.execute(query)
        await self.db.flush()