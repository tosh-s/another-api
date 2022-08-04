from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime

# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True

# class CreatePost(BaseModel):
#     title: str
#     content: str
#     published: bool = True

# class UpdatePost(BaseModel):
#     title: str
#     content: str
#     published: bool

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    

# class PostCreate extends PostBase
class PostCreate(PostBase):
    pass

# added this during user a/c creation and validation peice. 
class UserCreate(BaseModel):
	email: EmailStr
	password: str
    
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    # class config tells pydantic to use the sql alchemy model even though it is not
    # a dict. The app understands pydantic and dicts, postgres understands ORM or SQLalchemy
    class Config:
        orm_mode = True


# this class is for the response, after this is specified here
# http responses will only send back fields part of the class attributes.
# added owner_id at 8:15 after doing relational integrity.
class Post(PostBase):
    id: int
    title: str
    content: str
    published: bool = True
    owner_id: int
    created_at: datetime
    owner: UserOut  # added this at 8.37 after adding rel to models.py

    class Config:
        orm_mode = True
   

class UserLogin(BaseModel):
	email: EmailStr
	password: str


#after Outh2passwordrequest was implemented, created schemas for the token and token data
#so user requests are accompanied by token HH:mm 7:15
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

# added this at 10:30 after Votes Join
class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True
 
