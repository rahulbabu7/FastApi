from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI();



@app.get("/")  #@ is the decorator get is the http method / is the end point
# async def root():   #async is not must here because we are not doing any asynchronous jobs here
def root():  
    return {"message": "Welcome Guyz"}

@app.get("/posts")
def get_posts():
    return{" Message" : "This is the post section"}


#creating class
class CreatePost(BaseModel):
    title:str
    content:str
    isPublished:bool

    #the contents inside this class will only  taken fromm the post data  the key should be same here and there in the post

@app.post("/createposts")
def createPost(createPostDetails: CreatePost):
    print(createPostDetails)
    return{
        "message":"successfully created the post",
        # "createPostDetails" :createPostDetails
    }