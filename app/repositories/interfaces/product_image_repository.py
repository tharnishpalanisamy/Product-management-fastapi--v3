from typing import Protocol 
from models.product_image import ProductImage

class ProductImageRepositoryInterface(Protocol) :

    async def create(
            self, product_id: int,
            file_path: str, original_filename: str,
            content_type: str, file_type: str
    ) :
        ...
