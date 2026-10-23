from schemas.product import CategoryResponse 
from models.category import Category 
from models.product import Product
from sqlalchemy import select

class CategoryRepository:
    def __init__(self , db):
        self.db = db  
        

    async def get_all(self) :
        try : 
            statement = select(Category) 
            result = (await self.db.scalars(statement)).all() 

            return result 
        except : 
            raise 

