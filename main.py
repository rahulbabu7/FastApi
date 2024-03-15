# from fastapi import FastAPI
# from pydantic import BaseModel
# from random import randrange

# # from fastapi.middleware.cors import CORSMiddleware

# from starlette.middleware import Middleware
# from starlette.middleware.cors import CORSMiddleware



# middleware = [
#     Middleware(
#         CORSMiddleware,
#         allow_origins=['http://127.0.0.1:5500/'],
#         allow_credentials=True,
#         allow_methods=['*'],
#         allow_headers=['*']
#     )
# ]
# app = FastAPI(middleware=middleware);

# #creating class
# class CreatePost(BaseModel):
#     title:str
#     content:str
#     isPublished:bool =True  #if the user does not provided a value we use True for that
#     rating:int|None =None  #if the user does not provide a value its value is set to a default none
#  #the contents inside this class will only  taken fromm the post data  the key should be same here and there in the post

# #storing post details in memory
# myPosts = [{
#     "title":"title1",
#     "content":"content1",
#     "id":1
# },
# {
#     "title":"title2",
#     "content":"content2",
#     "id":2
# }]

# def findPost(id):
#     for post in myPosts:
#         if post["id"] == id:
#             return post



# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["http://127.0.0.1:5500/","http://localhost:5500/"],
# #     allow_credentials=True,
# #     allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
# #     allow_headers=["*"],
# # )   

# @app.get("/")  #@ is the decorator get is the http method / is the end point
# # async def root():   #async is not must here because we are not doing any asynchronous jobs here
# def root():  
#     return {"message": "Welcome Guyz"}

# @app.get("/posts")
# def get_posts():
#     return{" Message" : myPosts}

# @app.post("/createposts")
# async def createPost(createPostDetails: CreatePost):
#     # print(createPostDetails)
#     # print(createPostDetails.dict())  #converting the pydantic model to a python dictionary

#     #adding new post to myPost
#     myPostDict = createPostDetails.dict()
#     myPostDict['id'] = randrange(0,1000000)
#     myPosts.append(myPostDict)
#     return{
#         "message":"successfully created the post",
#         # "createPostDetails" :createPostDetails
#     }

# @app.get("/posts/{id}")  #id is the path parameter    THE PATH PARAMETER WILL ALWAYS BE A STRING
# def getPost(id:int):  #the id should be converted to int or it should take a value where it can be converted to int
#     # myPost = findPost(int(id))   #we need to convert the id to a int because in the dictionary it is of string  
#     #but here it is of type string so convert it to number
#     #we can avoid this by making the id in the dictionary as a string 
#     myPost = findPost(id) 
#     print(myPost)
#     return{
#         "post":myPost
#     }


from fastapi import FastAPI,Response,status,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from random import randrange

app = FastAPI()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"]
)

# Define data model
class CreatePost(BaseModel):
    title:str
    content:str
    isPublished:bool =True  #if the user does not provided a value we use True for that
    rating:int|None =None  #if the user does not provide a value its value is set to a default none
#  #the contents inside this class will only  taken fromm the post data  the key should be same here and there in the post

# Initialize posts
myPosts = [
    {"title": "title1", "content": "content1", "id": 1},
    {"title": "title2", "content": "content2", "id": 2}
]

# Generate random post ID
def generate_post_id():
    return randrange(0, 1000000)


#route to home
@app.get("/")
def home():
    return {
        'message':"welcome"
    }
# Route to create post
@app.post("/createposts",status_code=status.HTTP_201_CREATED)
async def create_post(create_post_details: CreatePost):
    post_data = create_post_details.dict()
    post_data["id"] = generate_post_id()
    myPosts.append(post_data)
    return {"message": "Post created successfully"}

# Route to get all posts
@app.get("/posts")
async def get_posts():
    return {"posts": myPosts}


def findPost(id):
    for post in myPosts:
        if post["id"] == id:
            return post



# Route to get post by ID
@app.get("/posts/{id}")  #id is the path parameter    THE PATH PARAMETER WILL ALWAYS BE A STRING
def getPost(id:int,response:Response):  #the id should be converted to int or it should take a value where it can be converted to int
    # myPost = findPost(int(id))   #we need to convert the id to a int because in the dictionary it is of string  
    #but here it is of type string so convert it to number
    #we can avoid this by making the id in the dictionary as a string 
    myPost = findPost(id) 
    if not myPost:
        # response.status_code=status.HTTP_404_NOT_FOUND  #setting the status code for error
        # return{'message':f"post with id {id} not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")    #detail is the msg to be printed to the user
    
    print(myPost)
    return{
        "post":myPost
    }


#delete post

@app.delete("/posts/{id}")
def deletePost(id:int):

    #delete the last entry of the list or delete using the id
    del myPosts[id];
    return{
        'msg': f"deleted post with {id}"
    }
