from fastapi import APIRouter , status , HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .. import schemas, models, oauth2
from ..database import getDB

"""Post router instance"""
router = APIRouter(
    tags=["Post"],
    prefix="/posts"
)

"""GET Method - Fetch all the posts"""
@router.get("/" , status_code=status.HTTP_200_OK , response_model=List[schemas.PostResponse])
def getAllPosts(db:Session=Depends(getDB) , limit:Optional[int]=10 , skip:Optional[int]=0 , search:Optional[str] = ""):

    posts = db.query(models.Post , func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit=limit).offset(offset=skip).all()

    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Posts found!")
    return posts


"""POST Method - Create's a post"""
@router.post("/" , status_code=status.HTTP_201_CREATED , response_model=schemas.Post)
def createPost(post:schemas.PostCreate , db:Session=Depends(getDB) , current_user:int=Depends(oauth2.getCurrentUser)):
    try:
        post = models.Post(owner_id=current_user.id,**post.dict())
        db.add(post)
        db.commit()
        db.refresh(post)
        return post

    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Post could not be created!")


"""GET Method - Fetch Post by ID"""
@router.get("/{id}" , status_code=status.HTTP_200_OK , response_model=schemas.PostResponse)
def getPost(id:int , db:Session=Depends(getDB)):
    post = db.query(models.Post , func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} does not exist!")
    return post


"""DELETE Method - Delete Post by ID"""
@router.delete("/{id}" , status_code=status.HTTP_202_ACCEPTED)
def deletePost(id:int , db:Session=Depends(getDB) , current_user:int=Depends(oauth2.getCurrentUser)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} does not exist!")

    if int(post.first().owner_id) != int(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="Not Authorized to perform requested action!")

    post.delete(synchronize_session=False)
    db.commit()
    return {"message" : f"Post with id:{id} is deleted"}
        

"""PUT Method - Update Post by ID"""
@router.put("/{id}" , status_code=status.HTTP_202_ACCEPTED , response_model=schemas.Post)
def updatePost(id:int , updatedPost:schemas.PostUpdate , db:Session=Depends(getDB) , current_user:int=Depends(oauth2.getCurrentUser)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} does not exist!")

    if int(post.first().owner_id) != int(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="Not Authorized to perform requested action!")

    post.update(updatedPost.dict(),synchronize_session=False)
    db.commit()
    return post.first()