class CategoryService:
    def __init__(self , db , repository) :
        self.repository = repository 
        self.db = db 

    async def get_all_categories(self) :
        return await self.repository.get_all() 

    async def get_total_sale(self , category_id) :
        return await self.repository.get_total_sale(category_id) 

    async def get_all_products(self, category_id) :
        return await self.repository.get_all_products(category_id) 
