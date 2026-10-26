from app.repositories.interfaces.user_repository import UserRepositoryInterface
from app.models import User
from app.core import hash_password
from datetime import datetime 

class AuthService: 
    def __init__(self,db , repository:UserRepositoryInterface) :
        self.db = db 
        self.repository = repository 

    async def authenticate_user(login_data) :
        pass 

    async def create_user(self, user_data) :
        hashed_password =  hash_password(user_data.password)
        user = User(
            email = user_data.email , 
            username = user_data.username ,
            hashed_password = hashed_password , 
            role = 'user' , 
            active = True         )
        return await self.repository.create(user) 