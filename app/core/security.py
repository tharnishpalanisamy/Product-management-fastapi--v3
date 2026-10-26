from pwdlib import PasswordHash 
from datetime import datetime , timedelta , timezone
from app.config import setting
import jwt

password_hash = PasswordHash.recommended() 

def hash_password(password:str) ->str :
    return password_hash.hash(password) 

def verify_password(password:str , hashed_password : str ) -> bool :
    return password_hash.verify(password , hashed_password) 

def create_access_token(user_id : int ) -> str :
    now = datetime.now(timezone.utc) 

    payload = {
        'sub' : str(user_id) , 
        'iat' : now , 
        'exp' : now + timedelta(
            minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    }

    return jwt.encode(
        payload=payload , 
        key = setting.JWT_SECRET_KEY , 
        algorithm=setting.JWT_ALGORITHM
    )