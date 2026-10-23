from typing import Protocol 
from models.product import Product 
from schemas.product import ProductCreate 

class ProductRepositoryInterface(Protocol) :

    async def create(self , data:ProductCreate ) -> Product :
        ...  

    async def get_all(self,filters) -> list[Product] : 
        ... 

    async def get_by_id(self, id ) -> Product: 
        ... 

    async def update(self , id , data) : 
        ... 

    async def restock(self , id, quantity) : 
        ... 

    async def get_summary(self, id) : 
        ... 

    async def delete(self , id) : 
        ... 