from pydantic import BaseModel, Field, EmailStr

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=8
    ) 


class UserCreate(BaseModel) : 
    username : str
    email : str 
    password : str 

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"