from fastapi import APIRouter 
from schemas.auth_schema import UserLogin

router = APIRouter(
    prefix='/Auth' , tags=['Authentication']
)


@router.post('/login') 
def login(login_data : UserLogin , ) : 
    pass 