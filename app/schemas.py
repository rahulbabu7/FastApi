from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
# from pydantic.types import conint


#request model  from client to backend
# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = (
#         True  # if user not provided published value then it is set to True
#     )
#     # rating: int | None

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

        
class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:int|None


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
    user_id:int
    user:User   # we are returning the user details like email ,id etc

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

class PostVote(BaseModel):
    post:Post
    votes:int
    class Config:
        from_attributes = True
#      since we deal with the convertion of object to dictionary we can comment the config class. the config class can be usefull when we have 1
#      Why it worked:

# Query returns: Posts ORM objects
# Schema expects: Post pydantic model
# from_attributes = True tells Pydantic: "Convert ORM object attributes to Pydantic model"
# FastAPI automatically does: Post.from_orm(posts_object) (or Post.model_validate() in Pydantic v2)

# No transformation needed! ✅



    
class Vote(BaseModel):
    post_id:int
    # dir: conint(ge=0,le=1)  # only allows 0 or 1
    dir:int = Field(...,ge=0,le=1,description="0 = remove vote, 1 = upvote")
