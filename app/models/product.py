from sqlalchemy import Integer , String , Numeric , ForeignKey
from sqlalchemy.orm import  Mapped , mapped_column , relationship 
# from models.category import Category 
# from models.product_image import ProductImage
from database.base import Base

class Product(Base) : 
    __tablename__ = 'products' 

    id : Mapped[int] = mapped_column(Integer , primary_key=True ) 
    product_name : Mapped[str] = mapped_column(String(150) , nullable=False)  
    cost_price : Mapped[float] = mapped_column(Numeric(12,2) , nullable=False) 
    quantity : Mapped[int] = mapped_column(Integer , nullable=False ) 
    category_id : Mapped[int] = mapped_column(Integer , ForeignKey('categories.id'),nullable=False) 

    category:Mapped['Category'] = relationship(
        back_populates='products'
    )

    files:Mapped[list['ProductImage']] = relationship(
        back_populates='product' , cascade='all, delete-orphan'
    )                                                                                     