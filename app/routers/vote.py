from fastapi import APIRouter , status , HTTPException, Depends
from sqlalchemy.orm import Session
from .. import schemas, models, oauth2
from ..database import getDB

"""Post router instance"""
router = APIRouter(
    tags=["Vote"],
    prefix="/vote"
)

"""POST Method - Like or Dislike a post"""
@router.post("/" , status_code=status.HTTP_201_CREATED)
def createVote(vote:schemas.Vote , db:Session=Depends(getDB) , current_user:int=Depends(oauth2.getCurrentUser)):
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"Post with id:{vote.post_id} does not exist!")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id , models.Vote.user_id ==current_user.id)
    if(vote.dir == 1):
        if vote_query.first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User:{current_user.id} has already voted on post:{vote.post_id}")
        else:
            vote = models.Vote(user_id=current_user.id,post_id=vote.post_id)
            db.add(vote)
            db.commit()
            db.refresh(vote)
            return {"message" : "Successfully added vote!"}
    else:
        if not vote_query.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist!")
        else:         
            vote_query.delete(synchronize_session=False)
            db.commit()
            return {"message" : "Successfully deleted vote!"}