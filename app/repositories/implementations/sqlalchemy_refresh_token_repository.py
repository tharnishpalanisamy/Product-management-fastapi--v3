
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

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
