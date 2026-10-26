from typing import TYPE_CHECKING
from decimal import Decimal
from sqlalchemy import String, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

# This block is only read by your code editor/type checker, ignoring runtime
if TYPE_CHECKING:
    from models.product import Product


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

