from datetime import datetime
from turtle import title
from typing import Optional
from pydantic import BaseModel,EmailStr,conint


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True 


#email validator already installl use import emailStr
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
     pass
    
class Post(PostBase):
    id: int   
    created_at: datetime
    owner_id: int
    owner: UserOut
    class Config:
        orm_mode = True


# #  {
# #         "Post": {
# #             "title": "titletestowner",
# #             "content": "This is test content for api test post request_withOwner",
# #             "created_at": "2022-04-13T05:14:22.685681+05:00",
# #             "id": 4,
# #             "published": false,
# #             "owner_id": 8
# #         },
# #         "votes": 1
# #     }
class PostOut(PostBase):
    Post: Post
    votes: int
    
    class Config:
        orm_mode = True

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None