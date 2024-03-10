from fastapi import FastAPI
from pydantic import BaseModel
from random import randrange

# from fastapi.middleware.cors import CORSMiddleware

from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware



middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=['http://127.0.0.1:5500/'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )
]
app = FastAPI(middleware=middleware);

#creating class
class CreatePost(BaseModel):
    title:str
    content:str
    isPublished:bool =True  #if the user does not provided a value we use True for that
    rating:int|None =None  #if the user does not provide a value its value is set to a default none
 #the contents inside this class will only  taken fromm the post data  the key should be same here and there in the post

#storing post details in memory
myPosts = [{
    "title":"title1",
    "content":"content1",
    "id":1
},
{
    "title":"title2",
    "content":"content2",
    "id":2
}]

def findPost(id):
    for post in myPosts:
        if post["id"] == id:
            return post



# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://127.0.0.1:5500/","http://localhost:5500/"],
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
#     allow_headers=["*"],
# )   

@app.get("/")  #@ is the decorator get is the http method / is the end point
# async def root():   #async is not must here because we are not doing any asynchronous jobs here
def root():  
    return {"message": "Welcome Guyz"}

@app.get("/posts")
def get_posts():
    return{" Message" : myPosts}

@app.post("/createposts")
async def createPost(createPostDetails: CreatePost):
    # print(createPostDetails)
    # print(createPostDetails.dict())  #converting the pydantic model to a python dictionary

    #adding new post to myPost
    myPostDict = createPostDetails.dict()
    myPostDict['id'] = randrange(0,1000000)
    myPosts.append(myPostDict)
    return{
        "message":"successfully created the post",
        # "createPostDetails" :createPostDetails
    }

@app.get("/posts/{id}")  #id is the path parameter    THE PATH PARAMETER WILL ALWAYS BE A STRING
def getPost(id:int):  #the id should be converted to int or it should take a value where it can be converted to int
    # myPost = findPost(int(id))   #we need to convert the id to a int because in the dictionary it is of string  
    #but here it is of type string so convert it to number
    #we can avoid this by making the id in the dictionary as a string 
    myPost = findPost(id) 
    print(myPost)
    return{
        "post":myPost
    }
 


# from starlette.applications import Starlette
# from starlette.middleware import Middleware
# from starlette.middleware.cors import CORSMiddleware
# from starlette.responses import JSONResponse
# from pydantic import BaseModel
# from random import randrange

# # Define middleware
# middleware = [
#     Middleware(
#         CORSMiddleware,
#         allow_origins=["http://127.0.0.1:5500"],
#         allow_credentials=True,
#         allow_methods=["POST"],  # You can specify specific methods if needed
#         allow_headers=["*"],  # You can specify specific headers if needed
#     )
# ]

# # Create Starlette app with middleware
# app = Starlette(middleware=middleware)

# # Define data model
# class CreatePost(BaseModel):
#     title: str
#     content: str
#     isPublished: bool = True
#     rating: int = None

# # Initialize posts
# myPosts = [
#     {"title": "title1", "content": "content1", "id": 1},
#     {"title": "title2", "content": "content2", "id": 2}
# ]

# # Generate random post ID
# def generate_post_id():
#     return randrange(0, 1000000)

# # Route to create post
# @app.route("/createposts", methods=["POST"])
# async def create_post(request):
#     data = await request.json()
#     data["id"] = generate_post_id()
#     myPosts.append(data)
#     return JSONResponse({"message": "Post created successfully"})

# # Route to get all posts
# @app.route("/posts")
# async def get_posts(request):
#     return JSONResponse({"posts": myPosts})

# # Route to get post by ID
# @app.route("/posts/{id}")
# async def get_post(request):
#     post_id = int(request.path_params["id"])
#     post = next((post for post in myPosts if post["id"] == post_id), None)
#     if post:
#         return JSONResponse({"post": post})
#     else:
#         return JSONResponse({"message": "Post not found"}, status_code=404)
