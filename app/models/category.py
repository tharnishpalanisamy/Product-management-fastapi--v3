from sqlalchemy import String , Integer , Numeric 
from decimal import Decimal 
from sqlalchemy.orm import Mapped , mapped_column , relationship
from database.base import Base 
# from models.product import Product

class Category(Base) :
    __tablename__ = 'categories' 

    id : Mapped[int] = mapped_column(
        Integer , primary_key=True 
    )

    name : Mapped[str] = mapped_column(
        String(100) , nullable=False , unique=True 
    )

    margin : Mapped[Decimal] = mapped_column(
        Numeric(10,2) , nullable=False 
    )

    products: Mapped[list["Product"]] = relationship(
        back_populates="category"
    )

