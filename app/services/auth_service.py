from app.repositories.interfaces.user_repository import UserRepositoryInterface
from app.models import User
from app.core import hash_password , verify_password , create_access_token
from datetime import datetime 
from app.exceptions import InvalidCredentialsException , InvalidRefreshTokenException


class AuthService: 
    def __init__(self,db , repository:UserRepositoryInterface , refresh_token_service) :
        self.db = db 
        self.repository = repository 
        self.refresh_token_service = refresh_token_service

    async def authenticate_user(self , login_data) : 
        user = await self.repository.get_by_email(login_data.email) 

        if not user :
            raise InvalidCredentialsException('Invalid username or password ') 
        authenticated = verify_password(
            login_data.password , user.hashed_password
        )

        access_token = create_access_token(user.id , user.role)    
        refresh_token = await self.refresh_token_service.issue_refresh_token(user.id) 

        if authenticated :
            return {
                'access_token' : access_token , 
                'refresh_token' : refresh_token,
                'token_type' : 'bearer' , 
                'user' : {
                    'id' : user.id , 
                    'username' : user.username , 
                    'email' : user.email 
                }
            } 
        
    async def create_user(self, user_data) :
        hashed_password =  hash_password(user_data.password)
        user = User(
            email = user_data.email , 
            username = user_data.username ,
            hashed_password = hashed_password , 
            role = 'user' , 
            active = True         )
        return await self.repository.create(user) 

    async def refresh_tokens(self , token ) : 
        user_id , new_refresh_token = await self.refresh_token_service.rotate_refresh_token(token)  

        user = await self.repository.get_by_id(user_id ) 

        if user is None :
            InvalidRefreshTokenException() 

        access_token = create_access_token(user.id , user.role) 

        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
        } 

