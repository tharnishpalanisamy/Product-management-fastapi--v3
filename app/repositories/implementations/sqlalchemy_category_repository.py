from app.schemas.product import CategoryResponse 
from app.models.category import Category 
from app.models.product import Product
from sqlalchemy import select , func , join

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

    async def get_total_sale(self , id ) :
        try :
            statement = select(
                Category.id ,
                Category.name , 
                func.sum(
                    (Product.cost_price * Category.margin ) * Product.quantity 
                ).label('Total sale')).join(
                    Product , Product.category_id == Category.id
                ).where(
                    Category.id == id 
                ).group_by(
                    Category.id ,
                    Category.name
                )
            

            result = (await self.db.execute(statement))

            return result.mappings().one_or_none()
        except Exception :
            raise 

    async def get_all_products(self , id) :
        try :
            statement = select(
                Product.id , Product.product_name , Product.quantity , 
                Product.cost_price , Category.name
                ).join(Category, Product.category_id == Category.id).where(
                    Product.category_id == id 
                )
            result = await self.db.execute(statement) 

            return result.mappings().all()  
        except Exception :
            raise 