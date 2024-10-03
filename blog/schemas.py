from pydantic import BaseModel 
from typing import List

class Blog(BaseModel):
    title: str 
    body: str 
    class Config():
        orm_mode = True 

# What things I want to see 
# class ShowBlog(BaseModel):
#     title: str 
#     class Config():
#         orm_mode = True 
    


class User(BaseModel):
    name: str
    email: str 
    password: str

class LittleShowUser(BaseModel):
    name: str 
    email: str 
    class Config():
        orm_mode = True 

class ShowUser(BaseModel):
    name: str
    email: str 
    blogs: List[Blog] 
    class Config():
        orm_mode = True 

# IF I want to everything accept ids 
class ShowBlog(BaseModel):
    title: str 
    body: str 
    creator: LittleShowUser 
    class Config():
        orm_mode = True 


class Login(BaseModel):
    username: str 
    password: str 


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None