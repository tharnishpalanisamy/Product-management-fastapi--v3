
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_db
from repositories.sqlalchemy_product_image_repository import ProductImageRepository
from services.product_image_service import ProductImageService


def get_product_image_repository(db: AsyncSession = Depends(get_db)) :
    return ProductImageRepository(db)

def get_product_image_service(
    db: AsyncSession = Depends(get_db), 
    repository :ProductImageRepository = Depends(get_product_image_repository)
) -> ProductImageService:
    

    product_service = ProductImageService(
        db,
        repository,
    )

    return product_service
