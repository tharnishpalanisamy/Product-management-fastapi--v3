from pydantic_settings import BaseSettings , SettingsConfigDict 
from pathlib import Path 

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings) :
    db_host:str 
    db_port:int 
    db_user:str 
    db_password:str 
    db_name:str 
    DATABASE_URL : str
    JWT_SECRET_KEY:str 
    JWT_ALGORITHM : str  = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES : int = 30 



    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

setting = Settings() 
