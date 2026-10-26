from app.models import User

class UserService:
    def __init__(self , db , repository) :
        self.db = db 
        self.repository = repository 

    async def get_all_users(self) -> list[User] :  
        return await self.repository.get_all()  

    async def delete_user(self , user_id) :
        return await self.repository.delete(user_id) 