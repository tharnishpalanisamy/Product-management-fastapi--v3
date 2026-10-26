from fastapi import APIRouter , Depends , HTTPException , status
from app.dependencies import get_user_service , get_current_user
from app.models import User
from app.schemas.user import UserResponse

router = APIRouter(
    prefix='/api/users' , tags = ['Users - Protected Routes '] 
)


@router.get('/' , response_model=list[UserResponse]) 
async def get_all_users(user:User = Depends(get_current_user) , service = Depends(get_user_service)) : 
    user_service = service 
    return await user_service.get_all_users()  


@router.delete('/{user_id}' , status_code=status.HTTP_204_NO_CONTENT) 
async def delete_user(
    user_id:int , 
    user:User = Depends(get_current_user) ,
    service = Depends(get_user_service)
):

    if user.role != 'admin' :
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    
    user_service = service 
    return await service.delete_user(user_id)