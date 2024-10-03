from fastapi import APIRouter ,FastAPI, Depends, status, Response, HTTPException
from .. import schemas, models
from sqlalchemy.orm import Session 
from typing import List 
from .. import database
from .. import hashing 

get_db = database.get_db 

router = APIRouter(
    prefix="/user", 
    tags=['users'], 
) 

@router.post('/', status_code = status.HTTP_201_CREATED)
def create_user(request: schemas.User, db : Session = Depends(get_db)):
    new_user = models.Users(name=request.name, email=request.email, pwd=hashing.Hash.bcrypt(request.password)) 
    db.add(new_user) 
    db.commit()
    db.refresh(new_user) 
    return new_user 

@router.get('/', status_code = status.HTTP_200_OK,response_model=List[schemas.ShowUser])
def show_user(db : Session = Depends(get_db)):
    users = db.query(models.Users).all() 
    return users


@router.get('/{id}', status_code = status.HTTP_200_OK, response_model=schemas.ShowUser)
def user_id(id, response: Response, db : Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {id} doesn't exist in the database")
        # response.status_code = status.HTTP_404_NOT_FOUND 
        # return {'detail' : f"Blog with {id} doesn't exist in the database" }
    return user
