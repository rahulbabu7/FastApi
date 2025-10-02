from fastapi import  HTTPException,status,Depends,APIRouter
from ..hashingPsd import hashedPassword
from .. import models,schemas
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=["Users"]   # grouping the api routes
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.User)
async def createUsers(user:schemas.UserCreate, db:Session = Depends(get_db)):
    user.password = hashedPassword(user.password)  #hashing the password 
    new_user = models.Users(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    
@router.get('/{id}',response_model= schemas.User)
async def getUserById(id:int,db:Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id ==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} not found")
    return user