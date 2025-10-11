from pydantic_settings import BaseSettings




class Settings(BaseSettings):
    secret_key:str
    algorithm:str
    expiration_time_minutes:int
    database_hostname:str
    database_port:str
    database_name:str
    database_username:str
    database_password:str
    frontend_url:str

    class Config:
        env_file =".env"



settings = Settings()
