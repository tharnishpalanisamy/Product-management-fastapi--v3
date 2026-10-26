from app.database.base import Base 
from sqlalchemy import String , Integer , DateTime , func , Boolean
from sqlalchemy.orm import Mapped , mapped_column 
from datetime import datetime 

class User(Base) : 
    __tablename__ = 'users' 
    id : Mapped[int] = mapped_column(
        Integer , primary_key= True , index=True 
    )
    username : Mapped[str] = mapped_column(
        String , nullable=False 
    )
    email : Mapped[str] = mapped_column(
        String(255) , nullable=False , unique=True 
    )
    role : Mapped[str] = mapped_column(
        String(20) , nullable=False , default='user' 
    )
    hashed_password:Mapped[str] = mapped_column(
        String(255) , nullable=False 
    )
    created_at:Mapped[datetime] = mapped_column(
        DateTime , nullable=False , default = datetime.now() ,server_default=func.now() 
    )
    active : Mapped[bool] = mapped_column(
        Boolean , nullable=False
    )
