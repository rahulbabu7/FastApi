import psycopg2
from fastapi import FastAPI, HTTPException, Response, status,Depends
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor
import time

from . import models
from .database import engine,get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)



app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = (
        True  # if user not provided published value then it is set to True
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

# my_posts: list[dict[str, str | int]] = [
#     {"title": "title of post 1", "content": "content of post 1", "id": 1},
#     {"title": "title of post 2", "content": "content of post 2", "id": 2},
# ]


# def find_post(id: int):
#     for post in my_posts:
#         if post["id"] == id:
#             return post


# def find_index_post(id: int):
#     for index, post in enumerate(my_posts):
#         if post["id"] == id:
#             return index


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
async def get_posts(db:Session = Depends(get_db)):
    posts = db.query(models.Posts).all()  # without all() it gives sql code
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post,db:Session = Depends(get_db)):
    new_post = models.Posts(**post.model_dump())  # unpacking dictionary
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  ## similar to the returning *

    # cursor.execute(""" INSERT INTO posts (title,content,publised) values (%s,%s,%s)""",(post.title,post.content,post.publised))
    # new_post = cursor.fetchone()
    # conn.commit()  #saving the new post to db
    return {"posts created successfully":new_post}


@app.get(f"/post{id}")
# def get_post(id:int,response:Response):
def get_post(id: int,db:Session = Depends(get_db)):

    # cursor.execute("""select * from posts where id = %s """,(str(id),))
    # posts = cursor.fetchone()
    
    post = db.query(models.Posts).filter(models.Posts.id ==id).first()
    
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return { "message":"post not found"}
        #
        # simpler
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="post not found"
        )
    return {"post": post}


@app.put("/posts{id}")
async def update_post(id: int, updated: Post,db:Session= Depends(get_db)):
    # cursor.execute("""update posts set title =%s, content=%s, publised=%s where id = %s  returning *""",(updated.title,updated.content,updated.published,str(id)))
    # post = cursor.fetchone()
    # conn.commit()
    # 
    post_query = db.query(models.Posts).filter(models.Posts.id ==id)  ##query for selecting the post 
    if not post_query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="post not found"
        )
    post_query.update(updated.model_dump(),synchronize_session=False)
    db.commit()
    
    return {"message": f"post with id {id} has been updated"}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int,db:Session=Depends(get_db)):
    # find the index in the array that has the required ID

    # cursor.execute("""delete from posts where id = %s  returning *""",(str(id),))
    # post = cursor.fetchone()
    # conn.commit()
    
    
    post_query = db.query(models.Posts).filter(models.Posts.id ==id)  ##query for selecting the post
    if post_query.first() == None:  #getting the first post
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="id not found"
        )
    post_query.delete(synchronize_session=False) #now deleting the post
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
