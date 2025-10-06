from fastapi import Depends, HTTPException,status
import jwt
from datetime import datetime,timedelta,timezone
from dotenv import load_dotenv
import os
from app.models import Users
from sqlalchemy.orm import Session
from app.database import get_db
from jwt.exceptions import InvalidTokenError
from app.schemas import TokenData


from fastapi.security import OAuth2PasswordBearer
oauth2_scheme =  OAuth2PasswordBearer(tokenUrl='login')  # used to get the token from the request


#secret key
# algorithm
# expiration time
# 
# get SECRET_KEY by running openssl rand -hex 32
# 
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
EXPIRATION_TIME_MINUTES = int(os.getenv("EXPIRATION_TIME_MINUTES"))

def create_access_token(data:dict)->str: #payload data
    to_encode:dict = data.copy()
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRATION_TIME_MINUTES)
    to_encode.update({'exp':expire})
    
    encoded_jwt_token:str = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    
    return encoded_jwt_token
    

def verify_access_token(token:str,credentials_exception:HTTPException)->TokenData:
    try:
        
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        
        user_id :int|None =payload.get("user_id")  #But payload.get("user_id") can return None if the key doesn't exist!
        
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(id=user_id)
        return token_data
    except InvalidTokenError:
        raise credentials_exception

def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db))->Users:
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"could not validate credentials",headers={"WWW_Authenticate":"Bearer"})
    
    
    token_data= verify_access_token(token,credentials_exception)
    print(token_data)
    user = db.query(Users).filter(Users.id==token_data.id).first()
    if user is None:
        raise credentials_exception
    return user  # returns a Users object