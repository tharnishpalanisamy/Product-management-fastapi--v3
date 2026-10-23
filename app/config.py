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

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

setting = Settings() 