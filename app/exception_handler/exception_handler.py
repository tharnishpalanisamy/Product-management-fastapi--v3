from fastapi import Request 
from fastapi.responses import JSONResponse 
from exceptions import (
    InvalidCategoryException , 
    DataBaseException , 
    ProductNotFoundException ,
    MaximumSizeExceeded , 
    EmptyFileException , 
    InvalidFileType
)

async def invalid_category_handler(request:Request , exc:InvalidCategoryException) :
    return JSONResponse(
        status_code=400 , 
        content={
            'success' : False , 
            'message' : str(exc)
        }
    )


async def product_not_found_handler(request:Request , exc:ProductNotFoundException) :
    return JSONResponse(
        status_code=404 , 
        content={
            'success' : False , 
            'message' : 'resource not found' ,
            'details' : str(exc) 
        }
    )

async def database_handler(request:Request , exc:DataBaseException) :
    return JSONResponse(
        status_code=500 , 
        content={
            'success' : False , 
            'message' : 'Unexpected error occured' , 
            'details' : str(exc)
        }
    )


async def database_handler(request:Request , exc:MaximumSizeExceeded) :
    return JSONResponse(
        status_code=413 , 
        content={
            'success' : False , 
            'message' : 'File size limit exceeded' , 
            'details' : str(exc)
        }
    )

async def database_handler(request:Request , exc:EmptyFileException) :
    return JSONResponse(
        status_code=400 , 
        content={
            'success' : False , 
            'message' : 'Bad request' , 
            'details' : str(exc)
        }
    )

async def database_handler(request:Request , exc:InvalidFileType) :
    return JSONResponse(
        status_code=415 , 
        content={
            'success' : False , 
            'message' : 'File type not supported' , 
            'details' : str(exc)
        }
    )

