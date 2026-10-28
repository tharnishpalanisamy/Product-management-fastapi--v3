from fastapi import APIRouter , Depends
from app.dependencies import get_category_service

router = APIRouter(
    prefix='/api/category' , tags=['category']
)


@router.get('/')
async def get_all(service = Depends(get_category_service)) :
    return await service.get_all_categories() 

@router.get('/{category_id}')
async def get_total_sale(category_id:int , service = Depends(get_category_service) ) :
    return await service.get_total_sale(category_id) 

@router.get('/{category_id}/all_products')
async def get_all_products(category_id:int , service = Depends(get_category_service)) :
    return await service.get_all_products(category_id) 