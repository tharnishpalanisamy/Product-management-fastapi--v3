from pydantic import BaseModel, Field, EmailStr

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=8
    )
