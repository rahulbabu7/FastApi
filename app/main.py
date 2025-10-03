# import psycopg2
from fastapi import FastAPI
# from psycopg2.extras import RealDictCursor
from . import models
from .database import engine
from .routers import posts,user,auth



models.Base.metadata.create_all(bind=engine) #create db tables
app = FastAPI()



# while True:
#     try:
#         conn = psycopg2.connect(
#             host='0.0.0.0',  # This should work if the app and postgres are on the same network
#             database='fastapi',
#             user='admin',
#             password='admin123',
#             cursor_factory=RealDictCursor
# # Returns rows as tuples.

# psycopg2.extras.RealDictCursor: Returns rows as dictionaries.

# psycopg2.extras.NamedTupleCursor: Returns rows as named tuples, so you can access columns like attributes (row.id, row.name, etc.).
#         )


#         cursor = conn.cursor()
#         print("Db up")
#         break
#     except Exception as error:
#         print("Db not connected")
#         print("error",error)
#         time.sleep(3)

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