from fastapi import APIRouter , status , HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, models, utils
from ..database import getDB

"""User router instance"""
router = APIRouter(
    tags=["User"],
    prefix="/users"
)

"""POST Method - Create's a User"""
@router.post("/" , status_code=status.HTTP_201_CREATED , response_model=schemas.UserResponse)
def createUser(user:schemas.UserBase , db:Session=Depends(getDB)):
    try:
        """hash the password"""
        user.password = utils.hashPassword(user.password)
        user = models.User(**user.dict())
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User could not be created!")

"""GET Method - Fetch all the users"""
@router.get("/" , status_code=status.HTTP_200_OK , response_model=List[schemas.UserResponse])
def getAllUsers(db:Session=Depends(getDB)):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Users found!")
    return users

"""GET Method - Fetch User by ID"""
@router.get("/{id}" , status_code=status.HTTP_200_OK , response_model=schemas.UserResponse)
def getUser(id:int , db:Session=Depends(getDB)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id:{id} does not exist!")
    return user

"""DELETE Method - Delete User by ID"""
@router.delete("/{id}" , status_code=status.HTTP_202_ACCEPTED)
def deleteUser(id:int , db:Session=Depends(getDB)):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id:{id} does not exist!")
    user.delete(synchronize_session=False)
    db.commit()
    return {"message" : f"User with id:{id} is deleted"}

"""PUT Method - Update User by ID"""
@router.put("/{id}" , status_code=status.HTTP_202_ACCEPTED , response_model=schemas.UserResponse)
def updateUser(id:int , updatedUser:schemas.UserUpdate , db:Session=Depends(getDB)):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id:{id} does not exist!")
    user.update(updatedUser.dict(),synchronize_session=False)
    db.commit()
    return user.first()        