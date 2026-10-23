from sqlalchemy.ext.asyncio import AsyncSession
from repositories.product_repository import ProductRepositoryInterface 


class ProductService:   
    def __init__(self , db:AsyncSession , repository:ProductRepositoryInterface ) :
        self.product_repository = repository 
        self.db = db 

    async def create_product(self , product_data) :
        return await self.product_repository.create(product_data)

    async def get_all_products(self , filters):
        return await self.product_repository.get_all(filters)  

    async def get_product_by_id(self , product_id : int) :
        return await self.product_repository.get_by_id(product_id)  

    async def update_product(self , product_id , product_data) :
        return await self.product_repository.update(product_id , product_data)

    async def patch_product(self, product_id , product_data) : 
        return await self.product_repository.patch(product_id , product_data)  

    async def delete_product(self, product_id) :
        return await self.product_repository.delete(product_id) 

    async def restock_product(self,product_id , product_data) :
        return await self.product_repository.restock(product_id , product_data.quantity)  

    async def display_product_summary(self, product_id) :
        return await self.product_repository.get_summary(product_id)