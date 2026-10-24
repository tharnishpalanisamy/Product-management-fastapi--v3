from pydantic import BaseModel , Field , EmailStr

class UserLogin:
    email : EmailStr 
    password : str = Field(min_length=8 , pattern=['^(?=.*[A-Z])(?=.*[0-9])(?=.*[@#$%^&*!])$']) 