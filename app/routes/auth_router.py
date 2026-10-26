from fastapi import APIRouter , Depends
from app.schemas.auth_schema import UserLogin , UserCreate
from app.dependencies.auth_dependency import get_auth_service

router = APIRouter(
    prefix='/Auth' , tags=['Authentication']
)


@router.post('/login') 
async def login(login_data : UserLogin , service = Depends(get_auth_service)) : 
    pass 

@router.post('/signup')
async def signup(user_data:UserCreate , service = Depends(get_auth_service) ) :  
    return await service.create_user(user_data)