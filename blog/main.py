from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas
from . import models
from . import database
from typing import List 
from sqlalchemy.orm import Session 
from . import hashing
from .routers import blog, user, authentication

app = FastAPI() 

models.Base.metadata.create_all(database.engine)

def get_db():
    db = database.SessionLocal() 
    try:
        yield db 
    finally:
        db.close() 

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentication.router)

