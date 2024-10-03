from fastapi import APIRouter ,FastAPI, Depends, status, Response, HTTPException
from .. import schemas, models
from sqlalchemy.orm import Session 
from typing import List 
from .. import database
from .. import oauth2

get_db = database.get_db 
get_current_user = oauth2.get_current_user

router = APIRouter(
    tags= ['blogs'], 
    prefix= "/blog"
) 


@router.get('/',response_model=List[schemas.ShowBlog])
def all_blogs(db : Session = Depends(get_db), get_current_user: schemas.User = Depends(get_current_user)):
    blogs = db.query(models.Blog).all() 
    return blogs


@router.post('/', status_code = status.HTTP_201_CREATED)
def create(request: schemas.Blog, db : Session = Depends(get_db), get_current_user: schemas.User = Depends(get_current_user)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit() 
    db.refresh(new_blog) 
    return new_blog

@router.get('/{id}', status_code = status.HTTP_200_OK, response_model=schemas.ShowBlog)
def blog_id(id,response: Response, db : Session = Depends(get_db), get_current_user: schemas.User = Depends(get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with {id} doesn't exist in the database")
        # response.status_code = status.HTTP_404_NOT_FOUND 
        # return {'detail' : f"Blog with {id} doesn't exist in the database" }
    return blog

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id,response: Response, db : Session = Depends(get_db), get_current_user: schemas.User = Depends(get_current_user)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False) 
    db.commit() 
   
    return {'Done'}


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(id, request: schemas.Blog, db : Session = Depends(get_db), get_current_user: schemas.User = Depends(get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id {id} not found')
    blog.update(request.dict())
    db.commit() 
