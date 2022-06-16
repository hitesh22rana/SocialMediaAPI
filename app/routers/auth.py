from fastapi import APIRouter , status , HTTPException, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import getDB
from .. import schemas, models, utils, oauth2

"""Auth router instance"""
router = APIRouter(
    tags=["Authentication"]
)

@router.post('/login' , response_model=schemas.Token)
def login(credentials:OAuth2PasswordRequestForm=Depends() , db:Session=Depends(getDB)):
    user = db.query(models.User).filter(models.User.email == credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    if not utils.verifyPassword(credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    """Token is Created"""
    token = oauth2.createAccessToken(data={"user_id":user.id})

    return {"access_token" : token , "token_type" : "bearer"}