from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, conint


"""Post Schema's"""
class PostBase(BaseModel):
    title : str
    content : str

class PostCreate(PostBase):
    published : bool = True

    class Config:
        orm_mode = True

class PostUpdate(PostBase):
    published : bool

    class Config:
        orm_mode = True


"""User Schema's"""
class UserBase(BaseModel):
    email : EmailStr
    password : str

class UserResponse(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime

    class Config:
        orm_mode = True

class UserUpdate(UserBase):
    pass

    class Config:
        orm_mode = True

class UserRelationship(BaseModel):
    id : int
    email : EmailStr

    class Config:
        orm_mode = True


"""Vote Schema"""
class Vote(BaseModel):
    post_id : int
    dir : conint(ge=0, le=1)


"""Login Schema's"""
class UserLogin(BaseModel):
    email : EmailStr
    password : str


"""Token Schema's"""
class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : Optional[str] = None


"""Relationship Schema's"""
class Post(PostBase):
    id : int
    published : bool
    created_at : datetime
    owner_id : int
    owner : UserRelationship

    class Config:
        orm_mode = True

class PostResponse(BaseModel):
    Post : Post
    votes : int
    
    class Config:
        orm_mode = True