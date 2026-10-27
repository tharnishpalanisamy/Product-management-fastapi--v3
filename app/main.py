from fastapi import FastAPI , Request
from app.api.routes.product_routes import router as product_router  
from app.api.routes.product_image_router import router as product_image_router 
from app.api.routes.cookie_router import router as cookie_router  
from app.api.routes.category_route import router as category_router 
from app.api.routes.user_routes import router as user_router
from app.api.routes.auth_router import router as auth_router
from app.api.routes.external_api_router import router as external_api_router
from app.exceptions import ProductNotFoundException , InvalidCategoryException , DataBaseException 
from app.exception_handler.exception_handler import (
    product_not_found_handler, invalid_category_handler , database_handler
)
import time 

app = FastAPI() 

@app.middleware('http') 
async def return_timing(request:Request , call_next) :
    start = time.perf_counter() 

    print(f'Incomonig request {request.method} {request.url.path} ') 
    response = await call_next(request) 
    process_time = time.perf_counter()  - start 
    print(f'Process timing {process_time}') 
    print(f"Status code: {response.status_code}")
    print(f"Processing time: {process_time:.4f} seconds")
    response.headers['time'] = str(process_time) 
    return response
    

app.include_router(product_router) 
# app.include_router(product_image_router) 
# app.include_router(cookie_router) 
# app.include_router(category_router) 
app.include_router(auth_router) 
app.include_router(user_router) 
app.include_router(external_api_router) 





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
