from models import Category 
from sqlalchemy.orm import selectinload 
from sqlalchemy import select, text 
from sqlalchemy.ext.asyncio import AsyncSession 
from exceptions import (
    InvalidCategoryException , DataBaseException , ProductNotFoundException
    )

from models.product import Product

class ProductRepository:
    def __init__(self , db:AsyncSession) :
        self.db = db 

    async def create(self , data) ->Product :
        
        try :

            statement = select(Category).where(
                    Category.id == data.category_id
                )
            
            category = await self.db.scalar(statement)
        
            if category is None :
                raise InvalidCategoryException(f"catergory not found ")
        
            product = Product(
                product_name = data.product_name , 
                cost_price = data.cost_price ,
                quantity = data.quantity ,
                category = category
            )
            
            self.db.add(product)
            await self.db.commit() 
            await self.db.refresh(product) 

            stmt = select(Product).options(
                selectinload(Product.category),
                selectinload(Product.files)
            ).where(
                Product.id == product.id
                ).order_by(
                    Product.id
                )
            
            fully_loaded_product = await self.db.scalar(stmt)
            return fully_loaded_product

        except InvalidCategoryException :
            raise 
        except Exception as error :
            await self.db.rollback() 
    
            raise DataBaseException(
                error 
            )
         


    async def get_all(self,filters) -> list[Product] :
        statement = select(Product).limit(
            filters['limit']
            ).offset(
                filters['offset']
                ).options(
            selectinload(Product.category) , 
            selectinload(Product.files)
        )
        products = (await self.db.scalars(statement=statement)).all() 
    
        return products  

    async def get_by_id(self, id ) -> Product:
        statement = select(Product).options(
            selectinload(Product.category) , 
            selectinload(Product.files)
        ).where(
            Product.id == id 
        )
        product =  await self.db.scalar(statement=statement)
    
        if product is None :
            raise ProductNotFoundException(
                'Item not found'
            )
    
        return product

    async def update(self , id , data) : 
        statement = select(Product).where(
                Product.id == id
            )
        product =  await self.db.scalar(statement) 
    
        if product is None :
            raise ProductNotFoundException(
                'Item not found'
            )
    
        try :
            product.product_name = data.product_name 
            product.cost_price = data.cost_price
            product.quantity = data.quantity
            product.category_id = data.category_id 
    
            await self.db.commit() 
            return {
                'message' : 'product updated successfully' , 
                'id' : id
            }
        except Exception :
            await self.db.rollback() 
            raise 

    async def patch(self, id , data) : 
        statement = select(Product).where(
                    Product.id == id
                )
        product = await self.db.scalar(statement) 
    
        if product is None :
            raise ProductNotFoundException(
                'Item not found'
            ) 
    
        try :
            if data.product_name is not None  :
                product.product_name = data.product_name  
            if data.cost_price is not None:
                product.cost_price = data.cost_price
            if data.quantity  is not None :
                product.quantity = data.quantity
            if data.category_id is not None:
                product.category_id = data.category_id 
    
            await self.db.commit() 
    
            return {
                'message' : 'product updated successfully' , 
                'id' : id
            }
        except :
            await self.db.rollback() 
            raise  

    async def delete(self , id) :
        statement = select(Product).where(
            Product.id == id
        )
        product = await self.db.scalar(statement) 
    
        if product is None :
            raise ProductNotFoundException(
                'Item not found'
            )
        try : 
            await self.db.delete(product) 
            await self.db.commit() 
            # self.db.refresh(product) 
    
            return {
                'message' : 'Product deleted successfully' , 
                'id' : id
            }
    
        except Exception as error  : 
            await self.db.rollback() 
            raise DataBaseException(
                        error 
                    ) 

    async def restock(self , id, quantity) : 
        statement = text("""
                        CALL restock_product(:id,:quantity) 
                        """)

        try :
            await self.db.execute(statement , {'id' : id , 'quantity' : quantity})   
            await self.db.commit() 

            return {
                'message' : f'Quantity of product {id} is increased by {quantity}' , 
                'id' : id 
            } 
        except Exception as error  :
            await self.db.rollback() 
            raise DataBaseException(
                        error 
                    )  


    async def get_summary(self, id) :
        statement = text("""
            SELECT *
            FROM display_summary(:id)
        """)

        result = await self.db.execute(
            statement,
            {"id": id}
        )

        return result.mappings().one_or_none()