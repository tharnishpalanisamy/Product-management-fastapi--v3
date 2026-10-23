from fastapi import APIRouter , Depends , status , Query 
from schemas.product import (
    ProductResponse , ProductCreate , ProductUpdate , ProductPatch , ProductRestockRequest
)
from repositories.sqlalchemy_product_repository import ProductRepository 
from services.product_service import ProductService
from dependencies import get_product_service 


router = APIRouter(prefix='/products' , tags = ['Products']) 


@router.get('/' , response_model=list[ProductResponse]) 
async def get_products( 
    limit:int | None =Query(default=10 , ge=1) ,
    offset:int | None = Query(default=0 , ge=0) ,
    service: ProductService = Depends(get_product_service) 
    ) :  

    product_service = service
    filters = {
        'limit' : limit , 
        'offset' : offset
    }
    return await product_service.get_all_products(filters) 

@router.get('/{product_id}' , response_model=ProductResponse) 
async def get_product(product_id:int ,service: ProductService = Depends(get_product_service) ) :
    product_service = service 
    
    return await product_service.get_product_by_id(product_id)

@router.post('/' , response_model=ProductResponse , status_code=status.HTTP_201_CREATED)    
async def create_product(product_data :ProductCreate ,service: ProductService = Depends(get_product_service)  ) :
    product_service = service
    return await product_service.create_product(product_data) 


@router.delete('/{product_id}') 

async def delete_item(product_id:int,service: ProductService = Depends(get_product_service)) : 
    product_service = service
    return await product_service.delete_product(product_id)


@router.put('/{product_id}') 
async def update_product(product_id : int , product_data:ProductUpdate,service: ProductService = Depends(get_product_service)  )  : 
    product_service = service
    return await product_service.update_product(product_id , product_data)

    

@router.patch('/{product_id}') 
async def patch_product(product_id:int , product_data:ProductPatch,service: ProductService = Depends(get_product_service)) :
    product_service = service
    return await product_service.patch_product(product_id , product_data)


@router.post('/{product_id}/restock') 
async def restock_product(product_id:int , product_data:ProductRestockRequest ,service:ProductService = Depends(get_product_service) ) : 
    product_service = service 

    return await product_service.restock_product(product_id , product_data)  


@router.post('/{product_id}/summary') 
async def display_summary(product_id:int,service:ProductService = Depends(get_product_service)) :
    product_service = service   
    result=  await product_service.display_product_summary(product_id=product_id)
    return dict(result)

    