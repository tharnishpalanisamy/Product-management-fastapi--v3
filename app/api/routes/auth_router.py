from fastapi import APIRouter , Depends , status
from app.schemas.auth_schema import UserLogin , UserCreate
from app.dependencies.auth_dependency import get_auth_service , get_current_user
from app.models import User

router = APIRouter(
    prefix='/Auth' , tags=['Authentication']
)



# @router.get('/me' ) 
# def get_me(current_user : User  = Depends(get_current_user)) :
#     return {
#         'id' : current_user.id , 
#         'username' : current_user.username , 
#         'email' : current_user.email 
#     }

@router.post('/login' , status_code=status.HTTP_201_CREATED) 
async def login(login_data : UserLogin , service = Depends(get_auth_service)) : 
    return await service.authenticate_user(login_data)

@router.post('/signup' , status_code=status.HTTP_201_CREATED)
async def signup(user_data:UserCreate , service = Depends(get_auth_service) ) :  
    return await service.create_user(user_data)