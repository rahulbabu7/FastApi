from fastapi import HTTPException, status,APIRouter,Depends
from sqlalchemy.orm import Session
from ..oauth2 import get_current_user
from ..models import Posts, Users, Votes
from ..schemas import Vote
from ..database import get_db

router = APIRouter(
     prefix="/vote",
    tags=["Vote"]
)

@router.post('/',status_code=status.HTTP_201_CREATED)
async def create_vote(vote:Vote,db:Session=Depends(get_db),current_user:Users=Depends(get_current_user)):

    post = db.query(Posts).filter(Posts.id==vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {vote.post_id} not found ")
    vote_query = db.query(Votes).filter(Votes.post_id==vote.post_id,Votes.user_id == current_user.id)  # checking if the vote exist in the system
    found_vote = vote_query.first()
    if vote.dir ==1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        new_vote = Votes(post_id=vote.post_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"Successfully voted"}  
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="vote not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message":"Successfully deleted voted"}
