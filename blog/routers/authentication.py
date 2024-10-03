from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, database, models
from sqlalchemy.orm import Session 
from ..hashing import Hash  
from ..token import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import datetime, timedelta, timezone


from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


get_db = database.get_db

router = APIRouter(
    tags=['auths']
)

@router.post('/login') 
def login(request: OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.email == request.username).first()
    if not user: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    if not Hash.verify(request.password, user.pwd):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentialssss")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return schemas.Token(access_token=access_token, token_type="bearer")
