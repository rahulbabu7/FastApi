from fastapi import FastAPI,Response,status,HTTPException
from pydantic import BaseModel
from random import randrange

from starlette.types import HTTPExceptionHandler
app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    publised: bool = (
        False  # if user not provided published value then it is set to false
    )
    rating: int | None


my_posts : list[dict[str,str|int]] = [
    {"title":"title of post 1", "content":"content of post 1" , "id":1},
    {"title":"title of post 2", "content":"content of post 2" , "id":2}
]


def find_post(id:int):
    for post in my_posts:
        if post["id"] ==id:
            return post
    
    
    
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
async def get_posts():
    return {"data": my_posts}


@app.post("/posts",status_code = status.HTTP_201_CREATED)
async def create_posts(post: Post):
    print(post)
    print(post.model_dump())   #.dict is deprecated
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0,1000)
    my_posts.append(post_dict)
    return {"posts created successfully":post_dict}


@app.get(f'/post{id}')
# def get_post(id:int,response:Response):
def get_post(id:int):
    
    post = find_post(id)
    
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return { "message":"post not found"}
        # 
        # simpler 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post not found")
    return {"post":post}


@app.put(f'/posts{id}')
async def update_posts(id:int):
    pass
    # my_posts.upda
    
