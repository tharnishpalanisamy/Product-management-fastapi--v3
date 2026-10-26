from pydantic import BaseModel , EmailStr 
from datetime import datetime

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    active: bool
    role: str
    created_at: datetime