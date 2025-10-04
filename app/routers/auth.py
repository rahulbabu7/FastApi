from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.hashingPsd import verifyPassword
# from app.schemas import UserLogin
from app.schemas import Token
from app.models import Users
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.oauth2 import create_access_token
router = APIRouter(
    tags=["Authentication"]
)

@router.post('/login',response_model=Token)
# def login(userCredentials:UserLogin,db:Session = Depends(get_db)):
def login(userCredentials:OAuth2PasswordRequestForm=  Depends(),db:Session = Depends(get_db)):
    user = db.query(Users).filter(Users.email == userCredentials.username).first()
    
    # userCredentials:OAuth2PasswordRequestForm=  Depends() 
    # this return only username and password


    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="user not found")
    if not verifyPassword(userCredentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
        
    # create token
    access_token = create_access_token(data = {"user_id":user.id})
    # return token
    return { "access_token": access_token , "token_type":"bearer"}
