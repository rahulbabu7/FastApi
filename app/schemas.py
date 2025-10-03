from datetime import datetime
from pydantic import BaseModel, EmailStr


#request model  from client to backend
# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = (
#         True  # if user not provided published value then it is set to True
#     )
#     # rating: int | None

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = (
        True  # if user not provided published value then it is set to True
    )
    # rating: int | None

class PostCreate(PostBase):
    #this has the same fields as the parent class
    pass

class PostUpdate(PostBase):
    # we are providing updates to all the fields
    pass


# response model from server to client
class Post(PostBase):
    id:int
    # title:str   these are getting from the parent class
    # content:str
    # published:bool
    created_at: datetime
    
    ## pydantic only works with dictionary. by adding the below config we can use if it is not a dictionary
    # Purpose: This is a configuration class within the Pydantic model.
    # orm_mode = True:   
    # When you set orm_mode = True, Pydantic will treat objects as dictionaries, allowing them to be serialized from ORM models (like SQLAlchemy or Django models) 
    # to Pydantic models.
    # By default, Pydantic assumes data comes in the form of a dictionary, but if you’re using an ORM model (like an SQLAlchemy model),
    # the data comes as an object with attributes rather than dictionary keys.
    # Setting orm_mode = True allows Pydantic to convert the ORM object to a Pydantic model by using the object’s attributes.
    class Config:
        # orm_mode = True     # in pydantic v1
          from_attributes = True  # in pydantic v2
          

class UserBase(BaseModel):
    email:EmailStr
    password:str
    
class UserCreate(UserBase):
    pass
    
# class UserLogin(UserBase):
#     pass
    
class User(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    class Config:
        from_attributes = True