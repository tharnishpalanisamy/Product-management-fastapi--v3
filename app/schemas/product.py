from pydantic import BaseModel , Field , ConfigDict 
from decimal import Decimal
from typing import Literal

class ProductCreate(BaseModel) :
    product_name : str = Field(min_length=2) 
    cost_price : Decimal = Field(ge = 1 , max_digits=12 , decimal_places=2) 
    quantity : int = Field(ge = 1 ) 
    category_id : int = Field(ge=1) 


class ProductResponse(BaseModel) :  
    model_config = ConfigDict(from_attributes=True) 
    id :int 
    product_name : str 
    cost_price : float 
    quantity : int  
    category_id:int
    category : CategoryResponse 
    files : list[ProductImageResponse] = [] 
    # stock_value : float  
    # margin : float 
    # selling_price : float 
    # sale_value : float
    # profit_per_item : float 
    # expected_profit : float 

class CategoryResponse(BaseModel) :
    model_config = ConfigDict(from_attributes=True) 

    id : int 
    name : str 
    margin : Decimal | None 

class ProductImageResponse(BaseModel) :
    id : int 
    file_type : str 
    original_filename : str 
    content_type : str 
    model_config = ConfigDict(from_attributes=True) 



class ProductUpdate(BaseModel) :
    product_name : str = Field(min_length=2) 
    cost_price : Decimal = Field(ge = 1 , max_digits=12 , decimal_places=2) 
    quantity : int = Field(ge = 1 ) 
    category_id : int = Field(ge=1) 

class ProductPatch(BaseModel) :
    product_name : str | None = Field(default=None , min_length=2) 
    cost_price : Decimal | None = Field( default=None ,ge = 1 , max_digits=12 , decimal_places=2) 
    quantity : int | None = Field( default=None ,ge = 1 ) 
    category_id : int | None = Field(default=None , ge=1) 


class ProductRestockRequest(BaseModel):
    quantity: int = Field(gt=0)


class ThemeRequest(BaseModel):
    theme: Literal["light", "dark"]