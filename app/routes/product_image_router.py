from fastapi import APIRouter , UploadFile , File  , Depends
from services.product_image_service import ProductImageService 
from dependencies import get_product_image_service

router = APIRouter(
    prefix='/productImages',
    tags = ['Product Documents']
)



@router.post('/{product_id}/images' ) 
async def create_product_image(product_id:int , file:UploadFile = File(...) , service:ProductImageService = Depends(get_product_image_service)) : 
    product_image_service = service  

    return await product_image_service.upload(
        product_id=product_id , 
        file=file , 
        file_type='image'
    )   


@router.post('/{product_id}/documents' ) 
async def create_product_document(product_id:int , file:UploadFile = File(...) ,service:ProductImageService = Depends(get_product_image_service) ) :
    product_image_service = service 

    return await product_image_service.upload(
            product_id=product_id , 
            file=file , 
            file_type='document'
        )

