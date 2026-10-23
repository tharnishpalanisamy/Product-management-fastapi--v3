
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import get_db
from repositories.implementations.sqlalchemy_category_repository import CategoryRepository
from services.category_service import CategoryService

def get_product_repository(db: AsyncSession = Depends(get_db)) : 
    return CategoryRepository(db)


def get_category_service(
    db: AsyncSession = Depends(get_db), 
    repository:CategoryRepository = Depends(get_product_repository)
) -> CategoryService:

    category_service = CategoryService(
        db,
        repository,
    )

    return category_service
