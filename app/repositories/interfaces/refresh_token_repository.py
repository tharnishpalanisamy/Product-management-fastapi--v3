from typing import Protocol

class RefreshTokenRepositoryInterface(Protocol): 

    async def create(self , data) : 
        ... 

    async def get_by_hash(self , hash) :
        ... 

    async def revoke(self , refresh_token , revoked_at) :
        ... 
