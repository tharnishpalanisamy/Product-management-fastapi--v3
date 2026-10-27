from fastapi import APIRouter , Depends , HTTPException , status
from app.dependencies import get_user_service , get_current_user , admin_required
from app.models import User
from app.schemas.user import UserResponse

router = APIRouter(
    prefix='/api/users' , tags = ['Users - Protected Routes '] 
)

@router.get('/me' , response_model=UserResponse) 
async def get_current_user(
    user:User = Depends(get_current_user) 
):
    return user 

@router.get('/' , response_model=list[UserResponse]) 
async def get_all_users(user:User = Depends(admin_required) , service = Depends(get_user_service)) : 
    user_service = service 
    return await user_service.get_all_users()  


@router.delete('/{user_id}' , status_code=status.HTTP_204_NO_CONTENT) 
async def delete_user(
    user_id:int , 
    user:User = Depends(admin_required) ,
    service = Depends(get_user_service)
):

    user_service = service 
    return await service.delete_user(user_id)