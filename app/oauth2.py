import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime,timedelta
from dotenv import load_dotenv
import os
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

def create_access_token(data:dict): #payload data
    to_encode = data.copy()
    
    expire = datetime.now() + timedelta(minutes=EXPIRATION_TIME_MINUTES)
    to_encode.update({'exp':expire})
    
    encoded_jwt_token = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    
    return encoded_jwt_token