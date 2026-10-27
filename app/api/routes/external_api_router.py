from fastapi import APIRouter , HTTPException
import httpx 
from app.clients.external_api_client import fetch_post

router = APIRouter(
    prefix='/api/external/posts' , tags=['External APIs']  
)

@router.get('/{post_id}') 
async def get_post(post_id:int ) :
    try : 
        return await fetch_post(post_id) 

    except httpx.HTTPStatusError as exc :
        raise HTTPException(
            status_code=502,
            detail="External API returned an error"
        ) from exc
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=504,
            detail="Could not communicate with external API"
        ) from exc
    
    