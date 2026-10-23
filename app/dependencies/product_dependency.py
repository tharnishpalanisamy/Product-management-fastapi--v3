
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_db
from repositories.sqlalchemy_product_repository import ProductRepository
from services.product_service import ProductService

def get_product_repository(db: AsyncSession = Depends(get_db)) : 
    return ProductRepository(db)


def get_product_service(
    db: AsyncSession = Depends(get_db), 
    repository:ProductRepository = Depends(get_product_repository)
) -> ProductService:

    product_service = ProductService(
        db,
        repository,
    )

    return product_service
