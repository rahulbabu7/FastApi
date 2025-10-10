from fastapi import  HTTPException,status,Depends,APIRouter,Response
from sqlalchemy import func
from .. import models,schemas
from ..database import get_db
from sqlalchemy.orm import Session
from app.oauth2 import get_current_user

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)



"""
@NOTE : Update the number of post the user can display at one time 
"""
@router.get("/",response_model=list[schemas.PostVote])  #The list[schemas.Post] means that the response will be a list of Post objects (i.e., a list of posts will be returned as the response).
async def get_posts(db:Session = Depends(get_db),get_current_user:models.Users = Depends(get_current_user),limit:int=10,skip:int=0,search:str|None=""):
    # posts = db.query(models.Posts).all()  # without all() it gives sql code
    # posts = db.query(models.Posts).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()    # we are getting the post which contains *** in the title and limiting the number of posts and also we can skip the first n posts
    # posts = db.query(models.Posts).filter(models.Posts.user_id==get_current_user.id).all()  # this gives only the users post
    results = db.query(models.Posts,func.count(models.Votes.post_id).label("votes")).join(models.Votes,models.Posts.id ==models.Votes.post_id,isouter=True).group_by(models.Posts.id).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()
    
#     Query returns:
#     [
#     (<Posts object>, 5),   # TUPLE with 2 items
#     (<Posts object>, 3),
#     (<Posts object>, 0),
# ]
#     Schema expects:
#     class PostVote(BaseModel):
#     post: Post        # Named field
#     votes: int        # Named field

    
# Why it breaks:

# Query returns: Tuples (post, votes)
# Schema expects: Objects/dicts with .post and .votes attributes
# from_attributes = True doesn't help because tuples don't have named attributes
# You need: {"post": post, "votes": votes}

# Transformation needed! ❌
# Summary
# ScenarioQuery ReturnsSchema ExpectsWorks?BeforePosts ORM objectPost pydantic model✅ Yes (auto-converted)After(Posts, int) tuplePostVote with .post & .votes❌ No (tuple vs dict)
# The key difference:

# Single ORM object → Auto-converts with from_attributes = True
# Tuple → Needs manual transformation to dict

# That's why you need the list comprehension for the votes endpoint but didn't need it before!
# Transform tuple → dictionary
    return [{"post":post,"votes":vote} for post,vote in results]


@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
async def create_posts(post: schemas.PostCreate,db:Session = Depends(get_db),get_current_user:models.Users = Depends(get_current_user)):  #make sure that the user is loggedIn
    new_post = models.Posts(user_id=get_current_user.id,**post.model_dump())  # unpacking dictionary
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  ## similar to the returning *

    # cursor.execute(""" INSERT INTO posts (title,content,publised) values (%s,%s,%s)""",(post.title,post.content,post.publised))
    # new_post = cursor.fetchone()
    # conn.commit()  #saving the new post to db
    return new_post


@router.get("/{id}",response_model=schemas.PostVote)
# def get_post(id:int,response:Response):
def get_post(id: int,db:Session = Depends(get_db),get_current_user:models.Users = Depends(get_current_user)):

    # cursor.execute("""select * from posts where id = %s """,(str(id),))
    # posts = cursor.fetchone()

    result  = db.query(models.Posts,func.count(models.Votes.post_id).label("votes")).join(models.Votes,models.Posts.id ==models.Votes.post_id,isouter=True).group_by(models.Posts.id).filter(models.Posts.id ==id).first()

    if not result:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return { "message":"post not found"}
        #
        # simpler
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="post not found"
        )
    post,votes = result  #Unpack and transform - post, votes = result then return as dict
    return {"post":post,"votes":votes}


@router.put("/{id}",response_model=schemas.Post)
async def update_post(id: int, updated: schemas.PostUpdate,db:Session= Depends(get_db),current_user:models.Users = Depends(get_current_user)):
    # cursor.execute("""update posts set title =%s, content=%s, publised=%s where id = %s  returning *""",(updated.title,updated.content,updated.published,str(id)))
    # post = cursor.fetchone()
    # conn.commit()
    #
    post_query = db.query(models.Posts).filter(models.Posts.id ==id)  ##query for selecting the post
    post_obj = post_query.first()
    if not post_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="post not found"
        )
    if post_obj.user_id != current_user.id:  # matching the foriegn key in posts and user id 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    post_query.update(updated.model_dump(),synchronize_session=False)
    db.commit()
#So post_query is a Query object, but post_query.first() is a single Posts instance.
    return post_obj


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int,db:Session=Depends(get_db),current_user:models.Users = Depends(get_current_user))->None:

    # cursor.execute("""delete from posts where id = %s  returning *""",(str(id),))
    # post = cursor.fetchone()
    # conn.commit()


    post_query = db.query(models.Posts).filter(models.Posts.id ==id)  ##query for selecting the post
    post_obj = post_query.first()
    if post_obj == None:  #getting the first post
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="id not found"
        )
    if post_obj.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    post_query.delete(synchronize_session=False) #now deleting the post

    db.commit()
    # return Response(status_code=status.HTTP_204_NO_CONTENT)
    return


#✅ Key points:

# Always use .first() to get the actual object from a Query.

# Query objects (post_query or post) are not the row itself; they are a builder for your SQL query.

# update() and delete() operate on the Query, not the object.
