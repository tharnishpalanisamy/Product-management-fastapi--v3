from app.database.base import Base
from sqlalchemy.orm import Mapped , mapped_column , relationship 
from sqlalchemy import Integer , String , ForeignKey , DateTime,func
from typing import TYPE_CHECKING 
from datetime import datetime , timezone

if TYPE_CHECKING : 
    from app.models import User


class RefreshToken(Base) :
    __tablename__ = 'refresh_tokens'

    id:Mapped[int] = mapped_column(
        Integer , primary_key=True 
    )
    user_id : Mapped[int] = mapped_column(
        Integer , ForeignKey('users.id' , ondelete="CASCADE") , index = True , nullable=False 
    )
    token_hash:Mapped[str] = mapped_column(
        String(64) , nullable=False , unique=True , index=True  
    )
    expires_at : Mapped[datetime] = mapped_column(
        DateTime(timezone=True) , nullable=False 
    )
    revoked_at : Mapped[datetime|None] = mapped_column(
        DateTime(timezone=True) , nullable=True 
    )
    replaced_by_id : Mapped[int|None] = mapped_column(
        Integer ,ForeignKey('refresh_tokens.id') , nullable=True 
    )
    created_at:Mapped[datetime] = mapped_column(
        DateTime(timezone=True) , nullable=False, default=datetime.now(timezone.utc) , server_default=func.now() 
    )

