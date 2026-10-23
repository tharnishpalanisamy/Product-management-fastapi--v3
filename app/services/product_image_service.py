from pathlib import Path 
from sqlalchemy.ext.asyncio import AsyncSession
from exceptions import InvalidFileType , MaximumSizeExceeded , EmptyFileException , ProductNotFoundException
from uuid import uuid4 
from repositories.sqlalchemy_product_image_repository import ProductImageRepository
from repositories.product_image_repository import ProductImageRepositoryInterface

UPLOAD_DIR = Path('upload/product') 

FILE_CONFIG = {
    'image' : {
        'types' :{
            'image/jpeg' : '.jpg' , 
            'image/png' : '.png' , 
            'image/webp' : '.webp' 
        } , 
        'max_size' : 5 * 1024 * 1024 
    }  , 
    'document' : {
        'types' : {
            'application/pdf' : '.pdf' , 
            'application/msword' : '.doc',
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx"
        } , 
        'max_size' : 10 * 1024 * 1024 
    }
}


class ProductImageService:
    def __init__(self,db:AsyncSession , repository:ProductImageRepositoryInterface) :
        self.product_image_repository = repository

    async def upload(self , product_id , file , file_type ) : 

        if file_type not in FILE_CONFIG :
            raise InvalidFileType('File type not supported ! ') 
        
        config = FILE_CONFIG[file_type]   

        if file.content_type not in config['types'] :
            raise InvalidFileType('File type not supported ! ')
        
        max_size = config['max_size'] 

        contents = await file.read(max_size + 1 ) 

        if len(contents) > max_size :
            raise MaximumSizeExceeded("File Size exceeded the limit")  

        if not contents :
            raise EmptyFileException('You have uploaded an empty file') 

        extension = config['types'][file.content_type] 
        filename = f"{uuid4().hex}{extension}" 

        UPLOAD_DIR.mkdir(parents=True , exist_ok=True ) 

        file_path = UPLOAD_DIR / filename 

        try :
            with file_path.open('wb') as destination :
                destination.write(contents) 

            result = await self.product_image_repository.create(
                product_id=product_id , 
                file_path=file_path.as_posix() , 
                original_filename=Path(file.filename or 'upload').name , 
                content_type= file.content_type , 
                file_type = file_type 
            ) 

            if result is None :
                raise ProductNotFoundException(f"product with id {product_id} not found ")  
            return result 
        except Exception :
            file_path.unlink(missing_ok=True)
            raise  
        finally :
            await file.close() 
