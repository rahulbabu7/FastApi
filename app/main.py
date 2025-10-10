
from fastapi import FastAPI
# from . import models
# from .database import engine
from .routers import posts,user,auth,vote

from app.config import settings  # schema for over env

#models.Base.metadata.create_all(bind=engine) #create db tables
app = FastAPI()


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
app.include_router(posts.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
