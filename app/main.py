from random import randrange
import psycopg2
from fastapi import FastAPI, HTTPException, Response, status
from psycopg2.errors import DatabaseError
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor
import time
app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    publised: bool = (
        False  # if user not provided published value then it is set to false
    )
    # rating: int | None

while True:
    try:
        conn = psycopg2.connect(
            host='0.0.0.0',  # This should work if the app and postgres are on the same network
            database='fastapi',
            user='admin',
            password='admin123',
            cursor_factory=RealDictCursor
        )
    
        
        cursor = conn.cursor()
        print("Db up")
        break
    except Exception as error:
        print("Db not connected")
        print("error",error)
        time.sleep(3)

my_posts: list[dict[str, str | int]] = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "title of post 2", "content": "content of post 2", "id": 2},
]


def find_post(id: int):
    for post in my_posts:
        if post["id"] == id:
            return post


def find_index_post(id: int):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            return index


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
async def get_posts():
    cursor.execute("""select * from posts""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post):
    
    cursor.execute(""" INSERT INTO posts (title,content,publised) values (%s,%s,%s)""",(post.title,post.content,post.publised))
    return {"posts created successfully"}


@app.get(f"/post{id}")
# def get_post(id:int,response:Response):
def get_post(id: int):

    cursor.execute(f"""select * from posts where id = {id}""")
    posts = cursor.fetchall()

    if not posts:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return { "message":"post not found"}
        #
        # simpler
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="post not found"
        )
    return {"post": posts}


@app.put("/posts{id}")
async def update_post(id: int, updated: Post):
    post = find_post(id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="post not found"
        )

    post_dict = updated.model_dump()
    index = find_index_post(id)
    post_dict["id"] = id
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="id not found"
        )

    my_posts[index] = post_dict

    return {"message": f"post with id {id} has been updated"}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):
    # find the index in the array that has the required ID

    index = find_index_post(id)

    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="id not found"
        )

    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
