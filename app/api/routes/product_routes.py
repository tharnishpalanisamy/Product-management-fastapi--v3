from fastapi import APIRouter , Depends , status , Query 
from app.schemas.product import (
    ProductResponse , ProductCreate , ProductUpdate , ProductPatch , ProductRestockRequest
)
from app.repositories.implementations.sqlalchemy_product_repository import ProductRepository 
from app.services.product_service import ProductService
from app.dependencies import get_product_service 
from app.models import User 
from app.dependencies import get_current_user , admin_required


router = APIRouter(prefix='/products' , tags = ['Products']) 


@router.get('/' , response_model=list[ProductResponse]) 
async def get_products( 
    product_name : str | None = Query(default=None) , 
    category_id : int | None = Query(default=None),  
    min_quantity : int | None = Query(default=None , ge=0) ,
    max_quantity : int | None = Query(default=None , gt=1), 
    min_cost : float | None = Query(default=None , gt=0 ), 
    max_cost : float | None= Query(default=None , gt=1) ,
    limit:int | None =Query(default=10 , ge=1) ,
    offset:int | None = Query(default=0 , ge=0) , 
    order_by : str = Query(default='id') ,
    sort_by : str = Query(default='asc') ,
    user:User = Depends(get_current_user) , 
    service: ProductService = Depends(get_product_service) 
    ) :  
    print("GET PRODUCTS ENDPOINT REACHED")
    product_service = service
    filters = {
        'product_name' : product_name , 
        'category_id' : category_id ,
        'min_quantity' : min_quantity ,
        'max_quantity' : max_quantity ,
        'min_cost' : min_cost ,
        'max_cost' : max_cost ,
        'limit' : limit , 
        'offset' : offset , 
        'order_by' : order_by , 
        'sort_by' : sort_by
    }
    return await product_service.get_all_products(filters) 

@router.get('/{product_id}' , response_model=ProductResponse) 
async def get_product(product_id:int ,service: ProductService = Depends(get_product_service),user:User = Depends(get_current_user)  ) :
    product_service = service 
    
    return await product_service.get_product_by_id(product_id)

@router.post('/' , response_model=ProductResponse , status_code=status.HTTP_201_CREATED)    
async def create_product(
    product_data :ProductCreate ,
    service: ProductService = Depends(get_product_service) ,
    user:User = Depends(admin_required)   ) :
    product_service = service
    return await product_service.create_product(product_data) 


@router.delete('/{product_id}') 

async def delete_item(
    product_id:int,
    service: ProductService = Depends(get_product_service) , 
    user:User = Depends(admin_required)
) : 
    product_service = service
    return await product_service.delete_product(product_id)


@router.put('/{product_id}') 
async def update_product(
    product_id : int , 
    product_data:ProductUpdate,
    service: ProductService = Depends(get_product_service),
    user:User = Depends(admin_required)   
)  : 

    product_service = service
    return await product_service.update_product(product_id , product_data)

    

@router.patch('/{product_id}') 
async def patch_product(
    product_id:int , 
    product_data:ProductPatch,
    service: ProductService = Depends(get_product_service),
    user:User = Depends(admin_required) 
) :
    product_service = service
    return await product_service.patch_product(product_id , product_data)


@router.post('/{product_id}/restock') 
async def restock_product(
    product_id:int , 
    product_data:ProductRestockRequest ,
    service:ProductService = Depends(get_product_service), 
    user:User = Depends(admin_required) 
) : 
    product_service = service 

    return await product_service.restock_product(product_id , product_data)  


@router.get('/{product_id}/summary') 
async def display_summary(
    product_id:int,
    service:ProductService = Depends(get_product_service),
    user:User = Depends(admin_required) 
) :
    product_service = service   
    result=  await product_service.display_product_summary(product_id=product_id)
    return dict(result)

    