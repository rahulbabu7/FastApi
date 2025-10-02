
from fastapi import  HTTPException,status,Depends,APIRouter,Response
from .. import models,schemas
from ..database import get_db
from sqlalchemy.orm import Session



router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)




@router.get("/",response_model=list[schemas.Post])  #The list[schemas.Post] means that the response will be a list of Post objects (i.e., a list of posts will be returned as the response).
async def get_posts(db:Session = Depends(get_db)):
    posts = db.query(models.Posts).all()  # without all() it gives sql code
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
async def create_posts(post: schemas.PostCreate,db:Session = Depends(get_db)):
    new_post = models.Posts(**post.model_dump())  # unpacking dictionary
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  ## similar to the returning *

    # cursor.execute(""" INSERT INTO posts (title,content,publised) values (%s,%s,%s)""",(post.title,post.content,post.publised))
    # new_post = cursor.fetchone()
    # conn.commit()  #saving the new post to db
    return new_post


@router.get("/{id}",response_model=schemas.Post)
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
    return post


@router.put("/{id}",response_model=schemas.Post)
async def update_post(id: int, updated: schemas.PostUpdate,db:Session= Depends(get_db)):
    # cursor.execute("""update posts set title =%s, content=%s, publised=%s where id = %s  returning *""",(updated.title,updated.content,updated.published,str(id)))
    # post = cursor.fetchone()
    # conn.commit()
    # 
    post_query = db.query(models.Posts).filter(models.Posts.id ==id)  ##query for selecting the post 
    if not post_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="post not found"
        )
    post_query.update(updated.model_dump(),synchronize_session=False)
    db.commit()
    
    return post_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
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

