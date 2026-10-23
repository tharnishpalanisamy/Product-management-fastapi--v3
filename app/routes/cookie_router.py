from fastapi import APIRouter , Request , Response 
from schemas.product import ThemeRequest
router = APIRouter(
    prefix='/cookie' , tags=['Cookie']
)

@router.post('/set') 
def set_cookie(data:ThemeRequest ,response:Response) :
    response.set_cookie(
        key = 'user_theme' , 
        value = data.theme , 
        max_age= 60 * 60 * 24 * 30 , 
        httponly=True , 
        secure=False , 
        samesite='lax' 
    )

    return {
        "message": f"Theme preference saved as {data.theme}",
        "theme": data.theme
    } 

@router.get('/theme') 
def get_theme(request : Request) :
    theme = request.cookies.get('user_theme' , 'light') 

    return {
        'theme' : theme 
    }



@router.delete('/theme')
def delete_theme(response: Response):
    response.delete_cookie(
        key='user_theme',
        httponly=True,
        secure=False,
        samesite='lax'
    )

    return {
        'message': 'Theme cookie deleted and reseted to default',
        'theme': 'light'
    }
