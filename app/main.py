from fastapi import FastAPI
from app.routes.product_routes import router as product_router  
from app.routes.product_image_router import router as product_image_router 
from app.routes.cookie_router import router as cookie_router  
from app.routes.category_route import router as category_router 
from app.routes.auth_router import router as auth_router
from app.exceptions import ProductNotFoundException , InvalidCategoryException , DataBaseException 
from app.exception_handler.exception_handler import product_not_found_handler, invalid_category_handler , database_handler

app = FastAPI() 


app.include_router(product_router) 
# app.include_router(product_image_router) 
# app.include_router(cookie_router) 
# app.include_router(category_router) 
app.include_router(auth_router) 




app.add_exception_handler(
    ProductNotFoundException , 
    product_not_found_handler
)

app.add_exception_handler(
    InvalidCategoryException , 
    invalid_category_handler
)

app.add_exception_handler(
    DataBaseException , 
    database_handler
)
