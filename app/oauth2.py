from fastapi import status , HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta
from . import schemas
from .config import settings

"""Secret Key"""
SECRET_KEY = settings.secret_key

"""Algorithm"""
ALGORITHM = settings.algorithm

"""Expiration Time"""
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

"""OAuth Schema"""
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def createAccessToken(data:dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verifyAccessToken(token:str, credentials_exception) -> int:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id:str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data

def getCurrentUser(token:str=Depends(oauth2_scheme)) -> int:
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentails", headers={"WWW-Authenticate" : "Bearer"})
    return verifyAccessToken(token=token, credentials_exception=credentials_exception)