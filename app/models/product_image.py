from database.base import Base 
from sqlalchemy import Integer , String , ForeignKey 
from sqlalchemy.orm import Mapped , mapped_column , relationship 
# from models import Product

class ProductImage(Base) : 
    __tablename__ = 'product_images' 

    id : Mapped[int] = mapped_column(
        Integer , primary_key=True 
    )

    product_id : Mapped[int] = mapped_column(Integer , ForeignKey('products.id' , ondelete='CASCADE') , nullable=False) 

    file_type : Mapped[str] = mapped_column(String(100) , nullable=False) 
    file_path : Mapped[str] = mapped_column(String(500) , nullable=False) 
    original_filename : Mapped[str] = mapped_column(String(255) , nullable=False ) 
    content_type : Mapped[str] = mapped_column(String(100) , nullable=False) 

    product:Mapped['Product']  = relationship(
        back_populates='files'
    )