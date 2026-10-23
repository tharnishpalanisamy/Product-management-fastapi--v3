class CategoryService:
    def __init__(self , db , repository) :
        self.repository = repository 
        self.db = db 

    async def get_all_categories(self) :
        return await self.repository.get_all() 