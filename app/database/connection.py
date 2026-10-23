from config import setting 
from sqlalchemy.ext.asyncio import (
    create_async_engine , 
    async_sessionmaker , 
    AsyncSession
)


engine = create_async_engine(setting.DATABASE_URL , echo=True) 

AsyncSessionLocal = async_sessionmaker(
    bind = engine , 
    class_=AsyncSession , 
    expire_on_commit=False  
)


async def get_db() :
    async with AsyncSessionLocal() as session:
        yield session




