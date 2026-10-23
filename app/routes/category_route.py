from fastapi import APIRouter , Depends
from dependencies import get_category_service

router = APIRouter(
    prefix='/category' , tags=['category']
)


@router.get('/')
async def get_all(service = Depends(get_category_service)) :
    return await service.get_all_categories() 