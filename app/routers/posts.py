from fastapi import  HTTPException,status,Depends,APIRouter,Response
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
@router.get("/",response_model=list[schemas.Post])  #The list[schemas.Post] means that the response will be a list of Post objects (i.e., a list of posts will be returned as the response).
async def get_posts(db:Session = Depends(get_db),get_current_user:models.Users = Depends(get_current_user),limit:int=10,skip:int=0,search:str|None=""):
    # posts = db.query(models.Posts).all()  # without all() it gives sql code
    posts = db.query(models.Posts).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()    # we are getting the post which contains *** in the title and limiting the number of posts and also we can skip the first n posts
    # posts = db.query(models.Posts).filter(models.Posts.user_id==get_current_user.id).all()  # this gives only the users post
    return posts


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


@router.get("/{id}",response_model=schemas.Post)
# def get_post(id:int,response:Response):
def get_post(id: int,db:Session = Depends(get_db),get_current_user:models.Users = Depends(get_current_user)):

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
    return post


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
